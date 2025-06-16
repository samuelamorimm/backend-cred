import re
from rest_framework import generics, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from django.core.validators import validate_email as django_validate_email
from logs.models import LogDeAcesso

class UserValidator:
    """Classe auxiliar para validações de usuário"""
    
    @staticmethod
    def validate_full_name(value):
        """Valida nome completo com espaços"""
        value = ' '.join(word.capitalize() for word in value.strip().split())
        
        if not value:
            raise ValidationError("O nome completo é obrigatório")
            
        if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', value):
            raise ValidationError("Use apenas letras e espaços")
            
        if len(value.split()) < 2:
            raise ValidationError("Digite nome e sobrenome")
            
        return value

    @staticmethod
    def validate_email(value):
        """Valida e normaliza email"""
        value = value.lower().strip()
        try:
            django_validate_email(value)
        except ValidationError:
            raise ValidationError("Email inválido")
            
        if User.objects.filter(email__iexact=value).exists():
            raise ValidationError("Este email já está em uso")
            
        return value

class AuthService:
    """Classe de serviço para operações de autenticação"""
    
    @staticmethod
    def log_access(email, action, result, details):
        """Registra tentativas de acesso"""
        LogDeAcesso.objects.create(
            user=email,
            acao=action,
            resultado=result,
            detalhes=details
        )

class RegisterSerializer(serializers.ModelSerializer):
    """Serializer para registro de usuários"""
    
    full_name = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password', 'password_confirmation']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {
                'validators': [UniqueValidator(
                    queryset=User.objects.all(),
                    message="Este email já está em uso"
                )]
            }
        }

    def validate(self, data):
        """Validação cruzada dos campos"""
        errors = {}
        
        # Valida senhas
        if data['password'] != data['password_confirmation']:
            errors['password_confirmation'] = ["As senhas não coincidem"]

        # Validações individuais
        try:
            validate_password(data['password'])
        except ValidationError as e:
            errors['password'] = e.messages
            
        try:
            UserValidator.validate_email(data['email'])
        except ValidationError as e:
            errors['email'] = [str(e)]
            
        try:
            UserValidator.validate_full_name(data['full_name'])
        except ValidationError as e:
            errors['full_name'] = [str(e)]
            
        if errors:
            raise serializers.ValidationError(errors)
            
        return data

    def create(self, validated_data):
        """Cria usuário com username automático"""
        full_name = validated_data.pop('full_name')
        email = validated_data.pop('email').lower().strip()
        
        # Gera username único a partir do email
        base_username = email.split('@')[0]
        username = base_username
        counter = 1
        
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        # Divide o nome completo
        names = full_name.split()
        first_name = ' '.join(names[:-1]) if len(names) > 1 else full_name
        last_name = names[-1] if len(names) > 1 else ''
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=validated_data['password'],
            first_name=first_name,
            last_name=last_name
        )
        
        return user

class RegisterView(generics.CreateAPIView):
    """Endpoint para registro de novos usuários"""
    
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            AuthService.log_access(
                request.data.get('email', ''),
                'Tentativa de Registro',
                'erro',
                str(serializer.errors)
            )
            return Response({
                "success": False,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            user = serializer.save()
            AuthService.log_access(
                user.email,
                'Registro',
                'sucesso',
                'Usuário registrado'
            )
            
            return Response({
                "success": True,
                "message": "Registro concluído com sucesso",
                "user": {
                    "full_name": f"{user.first_name} {user.last_name}".strip(),
                    "email": user.email
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            AuthService.log_access(
                request.data.get('email', ''),
                'Tentativa de Registro',
                'erro',
                str(e)
            )
            return Response({
                "success": False,
                "error": "Erro interno no servidor"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    """Endpoint para autenticação de usuários"""
    
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email", "").lower().strip()
        password = request.data.get("password", "")

        # Validação básica
        if not email or not password:
            AuthService.log_access(
                email or 'Não informado',
                'Tentativa de Login',
                'erro',
                'Credenciais não fornecidas'
            )
            return Response({
                "success": False,
                "error": "Email e senha são obrigatórios"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Busca usuário por email
            user = User.objects.get(email__iexact=email)
            user = authenticate(username=user.username, password=password)
            
            if not user:
                AuthService.log_access(
                    email,
                    'Tentativa de Login',
                    'erro',
                    'Senha incorreta'
                )
                return Response({
                    "success": False,
                    "error": "Credenciais inválidas"
                }, status=status.HTTP_400_BAD_REQUEST)
                
            # Gera ou obtém token
            token, created = Token.objects.get_or_create(user=user)
            AuthService.log_access(
                user.email,
                'Login',
                'sucesso',
                f'Token {"criado" if created else "reutilizado"}'
            )
            
            return Response({
                "success": True,
                "token": token.key,
                "user": {
                    "id": user.pk,
                    "full_name": f"{user.first_name} {user.last_name}".strip(),
                    "email": user.email
                }
            })
            
        except User.DoesNotExist:
            AuthService.log_access(
                email,
                'Tentativa de Login',
                'erro',
                'Email não encontrado'
            )
            return Response({
                "success": False,
                "error": "Credenciais inválidas"
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            AuthService.log_access(
                email,
                'Tentativa de Login',
                'erro',
                str(e)
            )
            return Response({
                "success": False,
                "error": "Erro interno no servidor"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
