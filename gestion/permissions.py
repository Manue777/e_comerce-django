from rest_framework.permissions import BasePermission
from .models import UsuarioModel

class SoloAdministradores(BasePermission):
    # message > sirve para cambiar el mensaje de error en el caso que no cumpla con los permisos suficientes
    message = 'Solamente los administradores pueden realizar esta accion'

    def has_permission(self, request, view):
        # request.user > me retornara el usuario registrado
        print(request.user)
        usuario:UsuarioModel = request.user

        # request.auth > me retornara el contexto que utilizo el usuario para la autenticacion (la token)
        print(request.auth)

        print(usuario.tipoUsuario)

        if usuario.tipoUsuario == 'ADMINISTRADOR':
            return True

        else:
            return False

class SoloStaff(BasePermission):
    message = 'Solamente el staff pueden realizar esta accion'

    def has_permission(self, request, view):
        usuario:UsuarioModel = request.user
        if usuario.tipoUsuario == 'STAFF':
            return True

        else:
            return False

class SoloTrabajador(BasePermission):
    message = 'Solamente el staff y administradores pueden realizar esta accion'

    def has_permission(self, request, view):
        usuario:UsuarioModel = request.user
        if usuario.tipoUsuario == 'STAFF' or usuario.tipoUsuario == 'ADMINISTRADOR':
            return True

        else:
            return False