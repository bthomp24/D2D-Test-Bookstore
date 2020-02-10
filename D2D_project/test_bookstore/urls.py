from django.urls import include, path
from .views import FileView
from django.conf.urls import url


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('upload/', FileView.as_view(), name='file-upload'),
]