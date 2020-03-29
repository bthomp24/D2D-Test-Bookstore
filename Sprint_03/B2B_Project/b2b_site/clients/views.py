from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy

from .forms import SearchManualForm, JsonForm

from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

# Create your views here.


class MainView(TemplateView):
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


def login(request):
    form = AuthenticationForm
    context = {
        "form": form
    }
    return render(request, 'registration/login.html', context=context)
