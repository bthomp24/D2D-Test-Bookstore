from django.urls import path
from . import views
from django.contrib import admin
from django.urls import include
from django.views.generic import RedirectView
from .views import MainView

urlpatterns = [
    path('', views.login, name = 'login'),
    path('search/', MainView.as_view(), name='search'),
]