from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('accounts/', include('django.contrib.auth.urls')), #https://docs.djangoproject.com/en/3.2/topics/auth/default/#module-django.contrib.auth.forms
    path('accounts/change_password', views.change_password, name="change_password"),
]
