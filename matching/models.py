# matching/models.py
from django.db import models

from users.models import User
from services.models import Service


class MatchRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed')
    )

    seeker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='match_requests_sent')
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='match_requests_received')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.seeker.username} - {self.provider.username} - {self.service.name}"
