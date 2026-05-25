from django.urls import path
from . import views

app_name = 'church'

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('history', views.history, name='history'),
    path('church_service', views.church_service, name='service'),
    path('vision', views.vision, name='vision'),
    path('mssion',views.mission, name='mission'),
    path('create-attendance', views.create_event_attendance, name='create-attendance'),
    path('attendance/<event_id>', views.event_attendance_list, name='attendance'),
]