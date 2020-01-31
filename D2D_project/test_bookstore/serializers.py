from rest_framework import serializers
from .models import Book

class BookSerializer (serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ('ISBN', 'title', 'author', 'description', 
                'publisher', 'release_date', 'price', 'series', 
                'volume_number',)