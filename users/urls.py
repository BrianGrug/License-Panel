from django.urls import path

from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from license_django import settings


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout')

]
