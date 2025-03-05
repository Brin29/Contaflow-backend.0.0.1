from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    message = 'Solo los administradores pueden acceder a esta vista.'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN'
    
class IsContador(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'CONTADOR'
    
class IsAuditor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'AUDITOR'
    
class IsCliente(permissions.BasePermission):
    message = 'Solo los clientes pueden acceder a esta vista.'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'CLIENTE'