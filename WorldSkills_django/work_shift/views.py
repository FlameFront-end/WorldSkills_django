from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import WorkShift, ShiftUser
from .serializers import WorkShiftSerializer


@api_view(['POST'])
def create_work_shift(request):
    serializer = WorkShiftSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def open_work_shift(request, id):
    try:
        work_shift = WorkShift.objects.get(id=id)
    except WorkShift.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if work_shift.active:
        return Response({"error": {"code": 403, "message": "Forbidden. There are open shifts!"}},
                        status=status.HTTP_403_FORBIDDEN)

    work_shift.active = True
    work_shift.save()
    serializer = WorkShiftSerializer(work_shift)
    return Response(serializer.data)


@api_view(['GET'])
def close_work_shift(request, id):
    try:
        work_shift = WorkShift.objects.get(id=id)
    except WorkShift.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not work_shift.active:
        return Response({"error": {"code": 403, "message": "Forbidden. The shift is already closed!"}},
                        status=status.HTTP_403_FORBIDDEN)

    work_shift.active = False
    work_shift.save()
    serializer = WorkShiftSerializer(work_shift)
    return Response(serializer.data)


@api_view(['POST'])
def add_user_to_shift(request, id):
    try:
        work_shift = WorkShift.objects.get(id=id)
    except WorkShift.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user_id = request.data.get('user_id', None)
    if user_id is None:
        return Response({"error": {"code": 400, "message": "Bad Request. 'user_id' field is required."}},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": {"code": 404, "message": "User not found."}}, status=status.HTTP_404_NOT_FOUND)

    if user in work_shift.users.all():
        return Response({"error": {"code": 403, "message": "Forbidden. The worker is already on shift!"}},
                        status=status.HTTP_403_FORBIDDEN)

    shift_user = ShiftUser(user=user, work_shift=work_shift)
    shift_user.save()

    return Response({"data": {"id_user": user.id, "status": "added"}}, status=status.HTTP_200_OK)
