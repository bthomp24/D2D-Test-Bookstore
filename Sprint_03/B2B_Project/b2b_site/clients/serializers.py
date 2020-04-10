from rest_framework import serializers
from .models import SearchCheckmate

class CheckmateSerializer (serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SearchCheckmate
        fields = ('title', 'authors', 'isbn')