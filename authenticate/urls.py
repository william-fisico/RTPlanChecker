from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('change_password', views.change_password, name='change_password'),
    path('register/', views.register_user, name='register'),
    path('login_permission_error/', views.login_permission_error, name="login_permission_error"),
]
