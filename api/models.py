from django.db import models
from django.contrib.auth.models import User

class Income(models.Model):
    title = models.CharField(max_length=50)
    amount = models.FloatField(blank=False, null=False)
    desc = models.CharField(max_length=200, blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source=models.CharField(max_length=50, default='Other')
    class Meta:
        ordering = ('-added_at',)

    def __str__(self):
        return self.title


class Expenses(models.Model):
    title = models.CharField(max_length=50)
    desc = models.CharField(max_length=250, blank=True)
    amount = models.FloatField(blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    categories=models.CharField(max_length=50, default='Other')

    class Meta:
        ordering = ('-added_at',)

    def __str__(self):
        return self.title
