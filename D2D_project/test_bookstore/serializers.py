from rest_framework import serializers
from .models import Book
from .models import File

class BookSerializer (serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ('ISBN', 'title', 'author', 'description', 
                'publisher', 'release_date', 'price', 'series', 
                'volume_number',)


class FileSerializer(serializers.ModelSerializer):
    class Meta():
        model = File
        fields = ('f', 'timestamp')
