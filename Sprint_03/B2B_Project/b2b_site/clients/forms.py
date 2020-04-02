from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class MultipleForm(forms.Form):
    action = forms.CharField(max_length=60, widget=forms.HiddenInput())


class SearchManualForm(MultipleForm):
    book_title = forms.CharField(required = False, max_length= 200, widget=forms.TextInput(attrs={'placeholder': 'Enter Title of the Book', 'size':40}))
    book_author = forms.CharField(required = False, max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter Author/s of the Book', 'size':40}))
    book_isbn = forms.CharField(required = False, max_length=13, min_length=10, widget=forms.TextInput(attrs={'placeholder': 'Enter ISBN number of the Book', 'size':40}))
    book_image_url = forms.URLField(required = False, max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Enter URL of the Book Cover', 'size':40}))
    

    def clean_search_form(self):
        book_title = self.cleaned_data['book_title']
        book_author = self.cleaned_data['book_author']
        book_isbn = self.cleaned_data['book_isbn']
        book_image_url = self.cleaned_data['book_image_url']
        

        #check if the isbn13 was entered or not
        if len(book_isbn) == 10:
            book_isbn = "978"+ book_isbn

        data = {"title": book_title, "author" : book_author, "isbn" : book_isbn, "image_url" : book_image_url}

        return data

class JsonForm(MultipleForm):
    json_code = forms.CharField(widget=forms.Textarea(attrs={'rows':40, 'cols':100}))

    def clean_json_code(self):
        json_code = self.cleaned_data['json_code']
        return json_code

class PasswordResetForm(forms.Form):
    old_password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'placeholder': 'Enter Title of the Book', 'size':40}))
    new_password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'placeholder': 'Enter Title of the Book', 'size':40}))
    confirm_new_password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'placeholder': 'Enter Title of the Book', 'size':40}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PasswordResetForm, self).__init__(*args, **kwargs)
    
    def clean_old_password(self):
        data = self.cleaned_data['old_password']

        if data != self.user.password:
            raise ValidationError(_('Invalid Password Entered'))
    def clean_confirm_new_password(self):
        data = self.cleaned_data['confirmed_new_password']
        new_password = self.cleaned_data['new_password']

        if data != new_password:
            raise ValidationError(_('Passwords do not Match.')) 