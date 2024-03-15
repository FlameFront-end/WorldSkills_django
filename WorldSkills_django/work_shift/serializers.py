from rest_framework import serializers

from .models import WorkShift, ShiftUser


class WorkShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkShift
        fields = '__all__'


class ShiftUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShiftUser
        fields = '__all__'
