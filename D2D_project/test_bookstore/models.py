from django.db import models

# Create your models here.
class Book(models.Model):
    ISBN = models.CharField(max_length=13, primary_key=True)
    title = models.CharField(max_length=200)
    primary_author = models.CharField(max_length=100)
    secondary_authors = models.CharField(max_length=200)
    description = models.TextField()
    publisher = models.CharField(max_length=200)
    release_date = models.CharField(max_length=200)
    price = models.CharField(max_length=50)
    series = models.CharField(max_length=200)
    volume_number = models.CharField(max_length=10)

    def __str__(self):
        return f' {self.ISBN}, {self.title}, {self.author}, {self.secondary_authors}'
