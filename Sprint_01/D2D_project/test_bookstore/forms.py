from django import forms


"""
args:
    a DjangoForm form: This is our constructor for creating
    the form that will serve as our search bar.
returns:
    not applicable
synopsis:
    A simple search bar that will be what the user uses to
    query the database for books.
"""
class searchBar(forms.Form):
    searcher = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'searchBar'}))