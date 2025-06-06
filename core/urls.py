from rest_framework import routers
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static



schema_view = get_schema_view(
    openapi.Info(
        title="API de Credenciamento - SESC",
        default_version='v1',
        description=(
            "API para gerenciamento de pedidos de credencial no SESC.\n\n"
            "Funcionalidades principais:\n"
            "- Consulta de credenciais por CPF e data de nascimento\n"
            "- Listagem de benefícios e notícias\n"
            "- Upload de documentos\n"
            "- Acompanhamento de pedidos de credencial\n"
        ),
        terms_of_service="https://www.sesc.com.br/termos-de-uso/",
        contact=openapi.Contact(name="Equipe de Suporte - SESC", email="suporte@sesc.com.br"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('cadastro.urls')),
    path('api/', include('pedidos.urls')),

    #Swagger --------------------------------------------------------------------------
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

