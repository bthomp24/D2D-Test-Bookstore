from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Site_Slug(models.Model):
    name = models.CharField(max_length=2, unique=True)
    site_name = models.CharField(max_length=100, default="you should probably have filled this out instead of seeing this")

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
    #queries = models.PositiveIntegerField(default=0)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class QueryInfo(models.Model):
    querynum = models.IntegerField(default = 0, null=False, blank=False)
    month = models.IntegerField(null=False, blank=False)
    year = models.IntegerField(null=False, blank=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)