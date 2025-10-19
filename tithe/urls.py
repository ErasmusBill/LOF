from django.urls import path
from . import views
from tithe.views import edit_tithe, user_dashboard

app_name = 'tithe'

urlpatterns = [
    # Authentication URLs
    path('login/', views.login_user, name='login_user'),
    path('register/', views.register_user, name='register_user'),
    path('logout/', views.logout_user, name='logout_user'),
    
    # Password Management URLs
    path('password-reset/', views.request_password_reset, name='request_password_reset'),
    path('reset-password/<str:token>/', views.reset_password, name='reset_password'),
    path('change-password/', views.change_password, name='change_password'),
    
    # User Profile URLs
    path('update-profile/', views.update_user, name='update_user'),
    
    # Dashboard URLs
    path('admin/dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('user/dashboard/', views.user_dashboard, name='user-dashboard'),
    
    # Tithe Management URLs
    path('tithe/add/', views.add_tithe, name='add_tithe'),
    path('tithe/list/', views.list_tithe, name='list-tithe'),
    path('edit/<int:tithe_id>/', views.edit_tithe, name='edit_tithe'),
    path('tithe/delete/<int:tithe_id>/', views.delete_tithe, name='delete_tithe'),
    path('tithe/user/', views.list_related_user, name='user-tithe'),
    
    # Home/Redirect URLs
    path('', views.login_user, name='home'),  
]