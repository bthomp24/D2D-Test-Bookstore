from django.urls import include, path
from .views import FileView
from .views import ProcessXML
from django.conf.urls import url


urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('upload/', FileView.as_view(), name='file-upload'),
    path('process/', ProcessXML.as_view(), name='file-process')
]