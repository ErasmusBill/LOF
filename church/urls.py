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
]