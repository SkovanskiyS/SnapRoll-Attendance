from django.contrib import admin
from django.urls import path
from .views import home_page, register_student, mark_attendance

urlpatterns = [
    path('', home_page, name='home_page'),
    path('register/', register_student, name='register_user'),
    path('attendance/', mark_attendance, name='mark_attendance'),
    path('admin/', admin.site.urls),
]



