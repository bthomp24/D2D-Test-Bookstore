from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy

from .forms import SearchManualForm, JsonForm

from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Site_Slug

# Create your views here.


class MainView(LoginRequiredMixin,TemplateView):
    template_name = "search.html"

    def get(self, request, *args, **kwargs):
        json_form = JsonForm(self.request.GET or None)
        manual_form = SearchManualForm(self.request.GET or None)

        context = self.get_context_data(**kwargs)
        context['json_form'] = json_form
        context['manual_form'] = manual_form

        return self.render_to_response(context)


class ManualFormView(FormView):
    form_class = SearchManualForm
    template_name = 'search.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        manual_form = self.form_class(request.POST)
        json_form = JsonForm

        if manual_form.is_valid():
            book_title = manual_form.cleaned_data['book_title']
            book_author = manual_form.cleaned_data['book_author']
            book_isbn = manual_form.cleaned_data['book_isbn']
            book_image_url = manual_form.cleaned_data['book_image_url']
            manual_form.save()

            book = {"title": book_title, "author": book_author,
                    "isbn": book_isbn, "image_url": book_image_url, "json": None}

            print(book)

            return book
        else:
            return self.render_to_response(self.get_context_data(manual_form=manual_form, json_form = json_form))

class JsonFormView(FormView):
    form_class = JsonForm
    template_name = 'search.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        json_form = self.form_class(request.POST)
        manual_form = SearchManualForm

        if json_form.is_valid():
            json_code = json_form.cleaned_data['json_code']

            json_form.save()

            book = {"title": None, "author": None,
                    "isbn": None, "image_url": None, "json": json_code}
            print(book)
            return book
        
        else:
            return self.render_to_response(self.get_context_data(json_form=json_form, manual_form = manual_form))

def search(request):
    book = {}

    if request.method == 'POST':
        form = SearchManualForm(request.POST)

        if form.is_valid():
            book_title = form.cleaned_data['book_title']
            book_author = form.cleaned_data['book_author']
            book_isbn = form.cleaned_data['book_isbn']
            book_image_url = form.cleaned_data['book_image_url']

            book = {"title": book_title, "author": book_author,
                    "isbn": book_isbn, "image_url": book_image_url, "json": "None"}

            print(book)

            return book

    else:
        form = SearchManualForm()

    context = {
        'form': form,
    }
    return render(request, 'search.html', context=context)

def results(request):

    site_list = Site_Slug.objects.order_by('name')

    for site in site_list:
        print(site.site_name)

    #Separate Book information
    book = {'name': 'HHGreg','author':'First Last','rating': 90.0,'cover':'https://upload.wikimedia.org/wikipedia/en/b/bb/Luigi_SSBU.png','link':'https://www.mariowiki.com/Luigi'}
    book2 = {'name': 'Sing-a-long','author':'First Last','rating': 87.0,'cover':'','link':'https://www.mariowiki.com/Luigi'}
    book3 = {'name': 'Why','author':'First Last','rating': 78.3,'link':'https://www.mariowiki.com/Luigi'}
    #Book list
    books = [book,book2,book3]
    #Site information
    site1 = {'name':'Kobo','books':books}

    book4 = {'name': 'Woweeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee','author':'First Last','rating': 97.1,'link':'https://www.mariowiki.com/Luigi'}
    book5 = {'name': 'Campfire','author':'First Name, Blah Blah, Jeff Smith','rating': 67.4,'cover':'https://upload.wikimedia.org/wikipedia/en/b/bb/Luigi_SSBU.png','link':'https://www.mariowiki.com/Luigi'}
    book6 = {'name': 'Eh','author':'First Last, Test Name','rating': 65.5,'link':'https://www.mariowiki.com/Luigi'}
    book62 = {'name': 'YEAAAH!','author':'Other Name','rating': 64.5,'link':'https://www.mariowiki.com/Luigi'}
    books2 = [book4,book5,book6,book62]
    site2 = {'name':'Google','books':books2}

    books3 = []
    site3 = {'name':'Livaria Cultura','books':books3}

    book7 ={'name': 'Bookis','author':'First Last','rating': 88.8,'link':'https://www.mariowiki.com/Luigi'}
    books4 = [book7]
    site4 = {'name':'Test Bookstore','books':books4}

    #Site list
    site_list = [site1,site2,site3,site4]

    context = {'site_list': site_list}

    return render(request,'results.html',context=context)


def login(request):
    form = AuthenticationForm
    context = {
        "form": form
    }
    return render(request, 'registration/login.html', context=context)

@login_required
def manage_account(request):
    context = {
    }
    return render(request, 'manage_account.html', context=context)

