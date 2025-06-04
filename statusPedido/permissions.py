from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Permissão para que apenas admins possam alterar,
    os demais podem apenas ler (GET).
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Permite métodos seguros (GET, HEAD, OPTIONS)
        return request.user and request.user.is_staff  # Só admin pode POST, PUT, DELETE
