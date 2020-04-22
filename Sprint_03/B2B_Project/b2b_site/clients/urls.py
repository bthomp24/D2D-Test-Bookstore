from django.urls import path
from . import views
from django.contrib import admin
from django.urls import include
from django.views.generic import RedirectView
from .views import MainView
from .views import CheckmateView
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.login, name = 'login_form'),
    path('search/', MainView.as_view(), name='search'),
    path('checkmate/', CheckmateView.as_view(), name='search-checkmate'),
    path('manage_account/', views.manage_account, name= 'manage_account'),
    path('loading/',TemplateView.as_view(template_name='loading.html')),
    path('results/', views.results, name='results'),
    path('query_report/', views.myFirstChart, name= 'query_report'),
    path('query_chart/', views.historicalChart, name= 'query_chart'),
]
