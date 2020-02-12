from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.views import generic

from .models import Book


def search(request):
    template = loader.get_template('test_bookstore/search.html')

    results = Book.objects.all()

    context = {
        'results': results,
    }

    return render(request, 'test_bookstore/search.html', context=context)

class bookDetail(generic.DetailView):
    model = Book

    def detail(self, request, primary_key):
        template = loader.get_template('test_bookstore/book_detail.html')

        book = get_object_or_404(Book, pk=primary_key)

        context = {
            'book': book
            }

        return render(request, 'test_bookstore/book_detail.html', context=context)