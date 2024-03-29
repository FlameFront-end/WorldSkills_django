from django.contrib import admin
from django.urls import path
from user.views import *
from work_shift.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-tort/user', UsersView.as_view()),
    path('api-tort/login', LoginView.as_view()),
    path('api-tort/logout', LogoutView.as_view()),

    path('api-tort/work-shift', create_work_shift),
    path('api-tort/work-shift/<int:id>/open', open_work_shift),
    path('api-tort/work-shift/<int:id>/close', close_work_shift),
    path('api-tort/work-shift/<int:id>/user', add_user_to_shift),
    path('api-tort/work-shift/<int:id>/order', view_orders_for_shift),
]
