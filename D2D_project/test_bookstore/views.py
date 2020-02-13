from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Book
from .forms import searchBar

from .search import Search_Query


def search(request):

    """
    if not request.method == 'POST':
        if 'search-persons-post' in request.session:
            request.POST = request.session['search-persons-post']
            request.method = 'POST'
            """
    
    if request.method == 'POST' or 'page' in request.GET:

        form = searchBar(request.POST)

        if form.is_valid():

            searcher = form.cleaned_data['searcher']

            results = Search_Query(searcher)

            paginator = Paginator(results, 5)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {
                'page_obj': page_obj,
                'results': results,
                'form': form,
                }
    else:
        
        form = searchBar()
        context = {
        'form': form,
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