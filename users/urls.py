from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'), #Registro de users
    path('api/login/', TokenObtainPairView.as_view(), name='login'), #Login de users
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), #Refresh de token
]
