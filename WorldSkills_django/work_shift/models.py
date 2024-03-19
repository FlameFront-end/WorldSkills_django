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


class Order(models.Model):
    shift = models.ForeignKey(WorkShift, on_delete=models.CASCADE)
    table = models.CharField(max_length=100)
    shift_workers = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order #{self.id} for {self.shift} on {self.created_at}"
