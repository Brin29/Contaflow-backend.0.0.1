from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import timedelta
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone
from django.contrib.auth.password_validation import validate_password
from .models import User, Company

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name' ,'username', 'password', 'role',  'phone_number', 'is_temp_password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CompaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'nit', 'address', 'economic_sector')

    def create(self, validated_data):
        company = Company.objects.create_company(**validated_data)
        return company

# TokenObtain personalizado para verificar la contraseña temporal
class CustomTokenObtainPairSerializar(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializar, self).validate(attrs)
        user = self.user

        data.update({'username': self.user.username})
        data.update({'password': self.user.password})
        data.update({'role': self.user.role})
        data.update({'is_temp_password': self.user.is_temp_password})

        if user.is_temp_password:
            expiration_date = user.temp_password_date + timedelta(hours=3)

            if timezone.now() > expiration_date:
                user.is_active = False
                user.save()
                raise AuthenticationFailed('Tu contraseña temporal ha expirado. Contacta al administrador')
            
            return ({
                'message': "Debes cambiar tu contraseña temporal.",
                'refresh': data.get('refresh'),
                'access': data.get('access'),
                'username': data.get('username'),
                'password': data.get('password'),
                'role': data.get('role'),
                'is_temp_password': data.get('is_temp_password')
            })
        
        return data
    
class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, write_only=True)

    # Para mas adelante
    # def validate_old_password(self, value):
    #     user = self.context['user']
    #     if not user.check_password(value):
    #         raise serializers.ValidationError('La contraseña actual es incorrecta')
    #     return value
    
    def validate_new_password(self, value):
        validate_password(value)
        return value