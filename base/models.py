from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    phoneNumber = models.BigIntegerField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=50, blank=True)
    lastName = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=250, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=timezone.now)

    def __str__(self) -> str:
        return f'{self.user.username}'
