from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer, CustomTokenObtainPairSerializar
from rest_framework_simplejwt.views import TokenObtainPairView
from django.template.loader import get_template
from rest_framework import permissions
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from .permissions import IsAdmin, IsAuditor, IsCliente, IsContador
from .serializers import ChangePasswordSerializer
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import User
import string
import secrets

User = get_user_model() 

# Vista de registro que maneja la administradora
# Solo en la fase de desarrollo
class RegisterView(APIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny] 

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

# Prueba de los endpoints
class UserView(APIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny] 
    
    def get(self, request, user_id):

        try:
            user = User.objects.get(id=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'})

class UsersView(APIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    
# Envio para agregar clientes y guardar en la base de datos
class sendEmail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):

        temp_password = generate_temp_password()
        request.data['password'] = temp_password

        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Contraseña temporal
        user.set_password(temp_password)
        user.is_temp_password = True
        user.temp_password_date = timezone.now()
        user.save()

        email = request.data['email']
        username = request.data['username']
        role = request.data['role']

        # datos del correo
        mail = create_email(
            email,
            'Enlace de Ingreso',
            'autorizacion.html',
            {
                'username': username,
                'email': email,
                'password': temp_password,
                'role': role,
            }
        )

        # Envio del correo
        mail.send(fail_silently=False)

        return Response({
            'message': 'Work'
        })

#  Cambio de contraseña
class ChangePassword(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # tomar al usuario
        user = request.user
        # validar las contraseñas
        serializer = ChangePasswordSerializer(data=request.data, context={'user': user})

        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.is_temp_password = False
            user.save()

            # Actualizar la sesion de usuario
            update_session_auth_hash(request, user)

            return Response ({'message': 'Contraseña cambiada exitosamente'})

        else:
            return Response({'contraseña': 'incorrecta'})

# Vista en la que solo el admnistrador tiene acceso
class AdminView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        content = {'message': 'Hello, Admin!'}
        return Response(content)
    
class ClientView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsCliente]

    def get(self, request):
        content = {'message': 'Hello, Client!'}
        return Response(content)
    

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializar

# ********* FUNCIONES **********

# creacion del correo
def create_email(user_email, subject, template_name, context):
    template = get_template(template_name)
    content = template.render(context)

    message = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=[
            user_email
        ],
        cc=[]
    )

    message.attach_alternative(content, 'text/html')
    return message

# creacion de la contraseña temporal
def generate_temp_password():
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(secrets.choice(alphabet) for _ in range(12))