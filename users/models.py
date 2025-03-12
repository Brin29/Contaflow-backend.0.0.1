from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    ROLES = (
        ('ADMIN', 'Admin'),
        ('CONTADOR', 'Contador'),
        ('AUDITOR', 'Auditor'),
        ('CLIENTE', 'Cliente Pyme')
    )
    phone_number = models.TextField(blank=True, null=True)
    is_temp_password = models.BooleanField(default=False, null=True)
    role = models.CharField(max_length=50, choices=ROLES, default='CLIENTE')
    temp_password_date = models.DateTimeField(null=True, blank=True)

class Company(models.Model):
    id = models.AutoField(primary_key=True)
    nit = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=255)
    economic_sector = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nit} - {self.address}"