from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer
from django.template.loader import get_template
from rest_framework import permissions
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from .permissions import IsAdmin, IsAuditor, IsCliente, IsContador
from django.utils import timezone
import string
import secrets

# Vista de registro que maneja la administradora
class RegisterView(APIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
    
class sendEmail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):

        temp_password = generate_temp_password()
        request.data['password'] = temp_password

        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        user.set_password(temp_password)
        user.is_temp_password = True
        user.temp_password_date = timezone.now()
        user.save()

        email = request.data['email']
        username = request.data['username']
        role = request.data['role']

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

        mail.send(fail_silently=False)

        return Response({
            'message': 'Work'
        })


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