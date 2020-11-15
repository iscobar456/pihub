from django.urls import path
from dashboard import views

urlpatterns = [
    path('', views.index),
    path('social', views.social),
    path('personal', views.personal),
    path('account', views.account)
]
