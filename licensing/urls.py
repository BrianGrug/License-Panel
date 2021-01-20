from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.index),
    path('add/', views.add),
    path('revoke/', views.revoke),
    path('validate/', views.validate),
    path('logs/', views.logs),
    path('discord/', views.g_discord),
]
