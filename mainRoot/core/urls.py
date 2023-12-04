from django.contrib import admin
from django.urls import path
from .views import home_page, register_student, mark_attendance, facecam_feed, frame1, frame2, get_names
from django.views.generic import TemplateView

urlpatterns = [
    path('', home_page, name='home_page'),
    path('register/', register_student, name='register_user'),
    path('attendance/', mark_attendance, name='mark_attendance'),
    path('frame1/', frame1, name='frame1'),
    path('frame2/', frame2, name='frame2'),
    path('facecam_feed', facecam_feed, name='facecam_feed'),
    path('get_names', get_names, name='get_names'),
    path('admin/', admin.site.urls),
]
