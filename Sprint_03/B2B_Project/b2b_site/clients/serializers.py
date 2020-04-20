from rest_framework import serializers

class SearchFields(object):
    def __init__(self, bookdata):
        self.bookdata = bookdata

class CheckmateSerializer (serializers.Serializer):
    bookdata = serializers.JSONField()
