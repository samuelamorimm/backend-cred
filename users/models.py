from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    # Seus campos personalizados aqui
    
    class Meta:
        db_table = 'custom_user'  # Nome personalizado para a tabela no banco de dados
    
    # Adicione esses campos para resolver o conflito
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',  # Nome personalizado
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',  # Nome personalizado
        related_query_name='user',
    )
