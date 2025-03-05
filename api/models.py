from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    ROLES = (
        ('ADMIN', 'Admin'),
        ('CONTADOR', 'Contador'),
        ('AUDITOR', 'Auditor'),
        ('CLIENTE', 'Cliente')
    )
    is_temp_password = models.BooleanField(default=False, null=True)
    role = models.CharField(max_length=50, choices=ROLES, default='CLIENTE')
    temp_password_date = models.DateTimeField(null=True, blank=True)