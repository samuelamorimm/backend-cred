from rest_framework import generics, serializers, status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth.password_validation import validate_password
from logs.models import LogDeAcesso

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este nome de usuário já está em uso.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email já está em uso.")
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("As senhas não coincidem.")
        validate_password(data['password'])  
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            #log caso login der erro
            LogDeAcesso.objects.create(
                user=email,
                acao='Tentativa de Login',
                resultado='erro',
                detalhes='Credenciais Inválidas'
            )
            return Response({"error": "Email ou senha inválidos."}, status=status.HTTP_400_BAD_REQUEST)
        

        user = authenticate(username=user.username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)

            #log caso login for bem sucedido
            LogDeAcesso.objects.create(
                user=user.email,
                acao='Tentativa de Login',
                resultado='sucesso',
                detalhes='Login bem-sucedido.'
            )

            return Response({"token": token.key})
        else:

            #log caso login der erro
            LogDeAcesso.objects.create(
                user=email,
                acao='Tentativa de Login',
                resultado='erro',
                detalhes='Credenciais Inválidas'
            )
            return Response({"error": "Email ou senha inválidos."}, status=status.HTTP_400_BAD_REQUEST)