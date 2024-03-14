import jwt
from time import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User

SECRET_KEY = 'your_secret_key_here'


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
