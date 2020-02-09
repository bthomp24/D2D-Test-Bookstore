from django.urls import include, path
#from rest_framework import routers
#from . import views
from .views import FileView
from django.conf.urls import url

# router = routers.DefaultRouter()
# router.register(r'views', views.BookViewSet)
#router.register(r'upload', FileView.as_view() ) #name='file-upload'

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    #path('views/', include(router.urls)),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    path('upload/', FileView.as_view(), name='file-upload'),
]