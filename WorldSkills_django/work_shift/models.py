from django.contrib.auth.models import User as AuthUser
from django.db import models


class WorkShift(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    active = models.BooleanField(default=False)
    users = models.ManyToManyField(AuthUser, through='ShiftUser')


class ShiftUser(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    work_shift = models.ForeignKey(WorkShift, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='added')
