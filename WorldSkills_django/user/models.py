from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50, null=True)
    surname = models.CharField(max_length=50, blank=True, null=True)
    patronymic = models.CharField(max_length=50, blank=True, null=True)
    login = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    photo_file = models.ImageField(upload_to='photos', blank=True, null=True)
    status = models.CharField(max_length=20, null=True)
    role = models.ForeignKey('Roles', on_delete=models.PROTECT, null=True)
    token = models.CharField(max_length=128, null=True)


class Roles(models.Model):
    title = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.title
