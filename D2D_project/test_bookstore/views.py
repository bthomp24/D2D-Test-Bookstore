from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def search(request):
    template = loader.get_template('test_bookstore/search.html')

    return render(request, 'test_bookstore/search.html')

def detail(request):
    template = loader.get_template('test_bookstore/detail.html')

    return render(request, 'test_bookstore/detail.html')