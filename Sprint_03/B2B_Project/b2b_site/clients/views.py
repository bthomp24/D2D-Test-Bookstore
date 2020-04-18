from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy

from .forms import SearchManualForm, JsonForm, QueryForm

from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from collections import OrderedDict
# Include the `fusioncharts.py` file that contains functions to embed the charts.

from .fusioncharts import FusionCharts
from .models import User, Company, QueryInfo, Site_Slug
from datetime import datetime
import json
import calendar
from django.template import loader

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import CheckmateSerializer
from .search_checkmate import search_checkmate

from .models import Site_Slug

# Create your views here.


def myFirstChart(request):
    current_month = datetime.now().month
    current_year = datetime.now().year

    queries = QueryInfo.objects.all()
    current_user = request.user
    temp_total = 0

    if current_user.is_superuser == False:
        current_company = current_user.user.company

        # Chart data is passed to the `dataSource` parameter, like a dictionary in the form of key-value pairs.
        dataSource = OrderedDict()

        # The `chartConfig` dict contains key-value pairs of data for chart attribute
        chartConfig = OrderedDict()
        chartConfig["caption"] = "Number of Queries made in this Month"
        chartConfig["subCaption"] = "Company: " + str(current_company)
        chartConfig["xAxisName"] = "Users"
        chartConfig["yAxisName"] = "Number of Queries"
        chartConfig["numberSuffix"] = " Queries"
        chartConfig["theme"] = "fusion"
        chartConfig["showValues"] = "1"
        chartConfig["labelDisplay"] = "auto"
        chartConfig["useEllipsesWhenOverflow"] = "1"

        dataSource["chart"] = chartConfig
        dataSource["data"] = []

        # The data for the chart should be in an array wherein each element of the array  is a JSON object having the `label` and `value` as keys.
        # Insert the data into the `dataSource['data']` list.

        for query in queries:
            print(query.user.company)
            print(query.month)
            print(query.year)
            if current_company == query.user.company and current_month == query.month and current_year == query.year:
                dataSource["data"].append(
                    {"label": query.user.name, "value": query.querynum})
                temp_total = temp_total + query.querynum

        # Create an object for the column 2D chart using the FusionCharts class constructor
        # The chart data is passed to the `dataSource` parameter.
        column2D = FusionCharts("column2d", "myFirstChart", "800",
                                "400", "myFirstchart-container", "json", dataSource)

        context = {
            "total": temp_total,
        }
        return render(request, 'query_report.html', {
            'output': column2D.render(),
            "total": temp_total,
        })

    else:
        dataSource = OrderedDict()
        dataSource["data"] = []
        dataSource["linkeddata"] = []
        companies = Company.objects.all()
        num = 0

        linkedchartConfig = OrderedDict()
        linkedchartConfig["caption"] = "Total Number of Queries Made in " + \
            calendar.month_name[current_month] + " "+str(current_year)
        linkedchartConfig["xAxisName"] = "Users"
        linkedchartConfig["yAxisName"] = "Number of Queries"
        linkedchartConfig["numberSuffix"] = " Queries"
        linkedchartConfig["theme"] = "candy"
        linkedchartConfig["showValues"] = "1"
        linkedchartConfig["labelDisplay"] = "auto"
        linkedchartConfig["palettecolors"] = "#5D62B5,#29C3BE,#F2726F,#FFC532,#67CDF2"

        for company in companies:
            temp_total = 0
            num = num + 1
            data = []
            linkedchartConfig["subCaption"] = "Company: " + str(company)
            for query in queries:
                if company == query.user.company and current_month == query.month and current_year == query.year:
                    temp_total = temp_total + query.querynum
                    data.append(
                        {"label": query.user.name, "value": query.querynum})

            dataSource["linkeddata"].append(
                {"id": "q"+str(num), "linkedchart": {"chart": linkedchartConfig, "data": data}})
            dataSource["data"].append(
                {"label": company.name, "value": temp_total, "link": "newchart-json-q"+str(num)})

    # The `chartConfig` dict contains key-value pairs of data for chart attribute
    chartConfig = OrderedDict()
    chartConfig["caption"] = "Total Number of Queries Made by Companies in " + \
        calendar.month_name[current_month] + " "+str(current_year)
    chartConfig["subCaption"] = "Click on columns to see Company Details"
    chartConfig["xAxisName"] = "Companies"
    chartConfig["yAxisName"] = "Number of Queries"
    chartConfig["numberSuffix"] = " Queries"
    chartConfig["theme"] = "candy"
    chartConfig["showValues"] = "1"
    chartConfig["labelDisplay"] = "auto"
    chartConfig["palettecolors"] = "#5D62B5,#29C3BE,#F2726F,#FFC532,#67CDF2"

    dataSource["chart"] = chartConfig

    column2D = FusionCharts("column2d", "myFirstChart", "800",
                            "400", "myFirstchart-container", "json", dataSource)

    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            month = form.cleaned_data['month']
            year = form.cleaned_data['year']
            company = form.cleaned_data['company']

            print("from view", month, year)
            request.session['month'] = month
            request.session['year'] = year
            request.session['company'] = company

            return redirect(reverse('query_chart'))
    else:
        form = QueryForm()

    return render(request, 'query_report.html', {
        'output': column2D.render(),
        "total": temp_total,
        "form": form,
    })


class MainView(LoginRequiredMixin, TemplateView):
    template_name = "search.html"

    def get(self, request, *args, **kwargs):
        json_form = JsonForm(self.request.GET or None)
        manual_form = SearchManualForm(self.request.GET or None)

        context = self.get_context_data(**kwargs)
        context['json_form'] = json_form
        context['manual_form'] = manual_form

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        if len(request.POST)==3:
            json_form = JsonForm(self.request.POST)
            manual_form = SearchManualForm()
        else:
            manual_form = SearchManualForm(self.request.POST)
            json_form = JsonForm()


        context = self.get_context_data(**kwargs)

        if json_form.is_valid():
            json_code = json_form.cleaned_data['json_code']

            request.session['json'] = json_code
            
            return redirect(reverse('loading_page'))
        elif manual_form.is_valid():
            book_title = manual_form.cleaned_data['book_title']
            book_isbn = manual_form.cleaned_data['book_isbn']
            book_author = manual_form.cleaned_data['book_author']
            book_image_url = manual_form.cleaned_data['book_image_url']
            manual_form.clean()

            request.session['book_title'] = book_title
            request.session['book_isbn'] = book_isbn
            request.session['book_author'] = book_author
            request.session['book_image_url'] = book_image_url 

   
            #return redirect(reverse('loading_page'))
            return redirect(reverse('results'))
        else:
            return self.render_to_response(self.get_context_data(manual_form=manual_form, json_form=json_form))

        return self.render_to_response(context)


class ManualFormView(FormView):
    form_class = SearchManualForm
    template_name = 'search.html'
    success_url = '/loading_page/'

    def post(self, request, *args, **kwargs):
        manual_form = self.form_class(request.POST)
        json_form = JsonForm()

        if manual_form.is_valid():
            book_title = manual_form.cleaned_data['book_title']
            book_author = manual_form.cleaned_data['book_author']
            book_isbn = manual_form.cleaned_data['book_isbn']
            book_image_url = manual_form.cleaned_data['book_image_url']

            book = {"title": book_title, "author": book_author,
                    "isbn": book_isbn, "image_url": book_image_url, "json": None}
            context = {
                'manual_form' : manual_form,
                'json_form' : json_form
            }

            return self.render_to_response(context)
        else:
            return self.render_to_response(self.get_context_data(manual_form=manual_form, json_form=json_form))


class JsonFormView(FormView):
    form_class = JsonForm
    template_name = 'search.html'
    success_url = '/loading_page/'

    def post(self, request, *args, **kwargs):
        json_form = self.form_class(request.POST)
        manual_form = SearchManualForm()

        if json_form.is_valid():
            json_code = json_form.cleaned_data['json_code']

            return self.render_to_response(self.get_context_data(manual_form=manual_form, json_form=json_form))

        else:
            return self.render_to_response(self.get_context_data(json_form=json_form, manual_form=manual_form))

class CheckmateView(APIView):
    parser_classes = (JSONParser, FormParser)
    
    def post(self, request, *args, **kwargs):

        serializer = CheckmateSerializer(data=request.data)
        if serializer.is_valid():
            json = serializer.data
            results = search_checkmate(json)
            return Response(results, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# def search(request):
#     book = {}

#     if request.method == 'POST':
#         form = SearchManualForm(request.POST)

#         if form.is_valid():
#             book_title = form.cleaned_data['book_title']
#             book_author = form.cleaned_data['book_author']
#             book_isbn = form.cleaned_data['book_isbn']
#             book_image_url = form.cleaned_data['book_image_url']

#             book = {"title": book_title, "author": book_author,
#                     "isbn": book_isbn, "image_url": book_image_url, "json": "None"}

#             print(book)

#             return book

#     else:
#         form = SearchManualForm()

#     context = {
#         'form': form,
#     }
#     return render(request, 'search.html', context=context)

def results(request):

    site_list = Site_Slug.objects.order_by('name')

    for site in site_list:
        print(site.site_name)

    book_title = request.session.get('book_title')
    book_isbn = request.session.get('book_isbn')
    book_author = request.session.get('book_author')
    book_image_url = request.session.get('book_image_url')
    json_code = request.session.get('json_code')

    print(book_author)
    print(book_image_url)
    print(book_isbn)
    print(book_title)
    print(json_code)

    # #Separate Book information
    # book = {'name': 'HHGreg','author':'First Last','rating': 90.0,'cover':'https://upload.wikimedia.org/wikipedia/en/b/bb/Luigi_SSBU.png','link':'https://www.mariowiki.com/Luigi'}
    # book2 = {'name': 'Sing-a-long','author':'First Last','rating': 87.0,'cover':'','link':'https://www.mariowiki.com/Luigi'}
    # book3 = {'name': 'Why','author':'First Last','rating': 78.3,'link':'https://www.mariowiki.com/Luigi'}
    # #Book list
    # books = [book,book2,book3]
    # #Site information
    # site1 = {'name':'Kobo','books':books}

    # book4 = {'name': 'Woweeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee','author':'First Last','rating': 97.1,'link':'https://www.mariowiki.com/Luigi'}
    # book5 = {'name': 'Campfire','author':'First Name, Blah Blah, Jeff Smith','rating': 67.4,'cover':'https://upload.wikimedia.org/wikipedia/en/b/bb/Luigi_SSBU.png','link':'https://www.mariowiki.com/Luigi'}
    # book6 = {'name': 'Eh','author':'First Last, Test Name','rating': 65.5,'link':'https://www.mariowiki.com/Luigi'}
    # book62 = {'name': 'YEAAAH!','author':'Other Name','rating': 64.5,'link':'https://www.mariowiki.com/Luigi'}
    # books2 = [book4,book5,book6,book62]
    # site2 = {'name':'Google','books':books2}

    # books3 = []
    # site3 = {'name':'Livaria Cultura','books':books3}

    # book7 ={'name': 'Bookis','author':'First Last','rating': 88.8,'link':'https://www.mariowiki.com/Luigi'}
    # books4 = [book7]
    # site4 = {'name':'Test Bookstore','books':books4}

    # #Site list
    # site_list = [site1,site2,site3,site4]

    context = {}#{'site_list': site_list}

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


def loading(request):
    book_title = request.session.get('book_title')
    book_isbn = request.session.get('book_isbn')
    book_author = request.session.get('book_author')
    book_image_url = request.session.get('book_image_url')
    json_code = request.session.get('json_code')

    print(book_author)
    print(book_image_url)
    print(book_isbn)
    print(book_title)
    print(json_code)
    context = {

    }
    return render(request, 'loading.html', context=context)


@login_required
def historicalChart(request):
    selected_month = int(request.session.get('month'))
    selected_year = int(request.session.get('year'))
    selected_company = request.session.get('company')
    queries = QueryInfo.objects.all()
    companies = Company.objects.all()

    dataSource = OrderedDict()
    dataSource["data"] = []
    dataSource["linkeddata"] = []

    num = 0

    linkedchartConfig = OrderedDict()
    linkedchartConfig["caption"] = "Total Number of Queries Made in " + \
        calendar.month_name[selected_month] + " "+str(selected_year)
    linkedchartConfig["xAxisName"] = "Users"
    linkedchartConfig["yAxisName"] = "Number of Queries"
    linkedchartConfig["numberSuffix"] = " Queries"
    linkedchartConfig["theme"] = "candy"
    linkedchartConfig["showValues"] = "1"
    linkedchartConfig["labelDisplay"] = "auto"
    linkedchartConfig["palettecolors"] = "#5D62B5,#29C3BE,#F2726F,#FFC532,#67CDF2"

    if selected_company == "None":
        for company in companies:
            temp_total = 0
            num = num + 1
            data = []
            linkedchartConfig["subCaption"] = "Company: " + str(company)
            for query in queries:
                if company == query.user.company and selected_month == query.month and selected_year == query.year:
                    temp_total = temp_total + query.querynum
                    data.append({"label": query.user.name,
                                 "value": query.querynum})

            dataSource["linkeddata"].append(
                {"id": "q"+str(num), "linkedchart": {"chart": linkedchartConfig, "data": data}})
            dataSource["data"].append(
                {"label": company.name, "value": temp_total, "link": "newchart-json-q"+str(num)})
    else:
        company = selected_company
        temp_total = 0
        num = num + 1
        data = []
        linkedchartConfig["subCaption"] = "Company: " + str(company)
        for query in queries:
            if company == str(query.user.company) and selected_month == query.month and selected_year == query.year:
                temp_total = temp_total + query.querynum
                data.append({"label": query.user.name,
                             "value": query.querynum})

        dataSource["linkeddata"].append(
            {"id": "q"+str(num), "linkedchart": {"chart": linkedchartConfig, "data": data}})
        dataSource["data"].append(
            {"label": company, "value": temp_total, "link": "newchart-json-q"+str(num)})

    # The `chartConfig` dict contains key-value pairs of data for chart attribute
    chartConfig = OrderedDict()
    chartConfig["caption"] = "Total Number of Queries Made by Companies " + \
        calendar.month_name[selected_month] + " "+str(selected_year)
    chartConfig["subCaption"] = "Click on columns to see Company Details"
    chartConfig["xAxisName"] = "Companies"
    chartConfig["yAxisName"] = "Number of Queries"
    chartConfig["numberSuffix"] = " Queries"
    chartConfig["theme"] = "candy"
    chartConfig["showValues"] = "1"
    chartConfig["labelDisplay"] = "auto"
    chartConfig["palettecolors"] = "#5D62B5,#29C3BE,#F2726F,#FFC532,#67CDF2"

    dataSource["chart"] = chartConfig

    column2D = FusionCharts("column3d", "myFirstChart", "800",
                            "400", "myFirstchart-container", "json", dataSource)
    return render(request, 'query_chart.html', {'output': column2D.render()})
