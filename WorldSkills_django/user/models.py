from django.db import models


class User(models.Model):
    login = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    token = models.CharField(max_length=128, blank=True, null=True)
