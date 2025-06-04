# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi

# @swagger_auto_schema(
#         operation_description="Upload de documento para um pedido de credencial.",
#         manual_parameters=[],
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             required=['pedido_credencial', 'tipo_documento', 'arquivo'],
#             properties={
#                 'pedido_credencial': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID do pedido'),
#                 'tipo_documento': openapi.Schema(type=openapi.TYPE_STRING, description='Tipo do documento'),
#                 'nome_documento': openapi.Schema(type=openapi.TYPE_STRING, description='Nome do documento (opcional)'),
#                 'arquivo': openapi.Schema(type=openapi.TYPE_FILE, description='Arquivo a ser enviado'),
#             },
#         ),
#         responses={
#             201: openapi.Response('Documento criado com sucesso'),
#             400: 'Erro de validação',
#             404: 'Pedido não encontrado',
#         }
#     )