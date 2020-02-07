from django.urls import path
from . import views

urlpatterns = [
    # Put the page URL's individually for the thing.
    path('', views.search, name='search'),
    path('details/', views.detail, name='detail'),

]
