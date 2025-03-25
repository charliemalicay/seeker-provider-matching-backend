# services/models.py
from django.db import models
from users.models import User


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    AVAILABILITY_CHOICES = (
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('both', 'Both')
    )

    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')
    category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability_type = models.CharField(max_length=10, choices=AVAILABILITY_CHOICES)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
