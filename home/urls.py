from django.urls import path
from django.contrib.auth.views import logout_then_login
from . import views

urlpatterns = [
    path('login', views.Login.as_view()),
    path('register', views.Register.as_view()),
    path('logout', logout_then_login),
    path('', views.homepage),
]