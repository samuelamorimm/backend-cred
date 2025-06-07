from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets, permissions

from cadastro.models import PedidoCredencial, EvolucaoPedido
from cadastro.serializers import PedidoCredencialSerializer, EvolucaoPedidoSerializer
from logs.models import LogDeAcesso


class AtualizarStatusPedidoView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pedido_id):
        novo_status = request.data.get('status')
        user_id = request.user.id if request.user.is_authenticated else None

        if not novo_status:
            return Response({'error': 'O campo status é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validar se o status é permitido
        status_validos = [choice[0] for choice in PedidoCredencial.STATUS_CHOICES]
        if novo_status not in status_validos:
            return Response(
                {'error': f'Status inválido. Escolha entre: {status_validos}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            pedido = PedidoCredencial.objects.get(id=pedido_id)
        except PedidoCredencial.DoesNotExist:
            return Response({'error': 'Pedido não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        # Atualiza o status atual do pedido
        pedido.status_pedido = novo_status
        pedido.save()

        # Registra na evolução
        EvolucaoPedido.objects.create(
            pedido_credencial=pedido,
            status_evolucao=novo_status,
            user_id=user_id
        )

        #log para caso atualização do pedido der certo
        LogDeAcesso.objects.create(
            user=request.user,
            acao='Alteração de status',
            resultado='sucesso',
            detalhes='...'
        )

        return Response({'message': f'Status atualizado para {novo_status} com sucesso.'}, status=status.HTTP_200_OK)
