from django.db import models

# Create your models here.

class Site_Slug(models.Model):
    name = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.name

class Company(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    slugs = models.ManyToManyField(Site_Slug)

    def display_slug(self):
        return ', '.join([slug.name for slug in self.slugs.all()])
    
    def __str__(self):
        return self.name

class User(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='users')
    queries = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name