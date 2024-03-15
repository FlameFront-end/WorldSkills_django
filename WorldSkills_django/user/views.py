from datetime import time

import jwt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Roles

SECRET_KEY = 'your_secret_key_here'


class UsersView(APIView):
    def post(self, request):
        data = request.data
        required_fields = ['name', 'login', 'password', 'role_id']

        if not all(field in data for field in required_fields):
            return Response({"error": {"code": 400, "message": "Name, login, password, and role_id are required"}},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            photo_file = request.FILES['photo_file']
        except KeyError:
            photo_file = None

        if User.objects.filter(login=data['login']).exists():
            return Response({"error": {"code": 400, "message": "Login already exists"}},
                            status=status.HTTP_400_BAD_REQUEST)

        if not Roles.objects.filter(id=data['role_id']).exists():
            return Response({"error": {"code": 400, "message": "Role does not exist"}},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create(name=data['name'], login=data['login'], password=data['password'],
                                       role_id=data['role_id'], photo_file=photo_file)
        except Exception as e:
            return Response({"error": {"code": 500, "message": str(e)}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"data": {"id": user.id, "status": "created"}}, status=status.HTTP_201_CREATED)

    def get(self, request):
        users = User.objects.all()
        users_data = []
        for user in users:
            user_data = {
                "id": user.id,
                "name": user.name,
                "login": user.login,
                "status": user.status,
                "group": user.role.title if user.role else None
            }
            users_data.append(user_data)

        return Response({"data": users_data}, status=status.HTTP_200_OK)


class LoginView(APIView):
    def post(self, request):
        login = request.data.get('login')
        if not login:
            return Response({"error": {"code": 400, "message": "Login is required"}},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(login=login).first()
        if not user:
            return Response({"error": {"code": 401, "message": "Authentication failed"}},
                            status=status.HTTP_401_UNAUTHORIZED)

        token = generate_token(user.id)
        user.token = token
        user.save()
        return Response({"data": {"user_token": token}}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def get(self, request):
        token = request.headers.get('Authorization')
        if not token:
            return Response({"error": {"code": 400, "message": "Token is required in the Authorization header"}},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(token=token)
        except User.DoesNotExist:
            return Response({"error": {"code": 404, "message": "User not found"}}, status=status.HTTP_404_NOT_FOUND)

        user.token = None
        user.save()
        return Response({"message": "User logged out successfully"}, status=status.HTTP_200_OK)


def generate_token(user_id, expiration_time=3600):
    payload = {
        'user_id': user_id,
        'exp': time() + expiration_time
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token
