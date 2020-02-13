from django import forms

class searchBar(forms.Form):
    searcher = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'searchBar'}))