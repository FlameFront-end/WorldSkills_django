from django.contrib import admin
from django.urls import path

from user.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-tort/login', LoginView.as_view()),
    path('api-tort/logout', LogoutView.as_view()),
]
