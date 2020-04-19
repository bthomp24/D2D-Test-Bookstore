from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import Company

class MultipleForm(forms.Form):
    action = forms.CharField(required=False, max_length=60, widget=forms.HiddenInput())


class SearchManualForm(MultipleForm):
    book_title = forms.CharField(required = False, max_length= 200, widget=forms.TextInput(attrs={'placeholder': 'Enter Title of the Book', 'size':40}))
    book_author = forms.CharField(required = False, max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter Author/s of the Book', 'size':40}))
    book_isbn = forms.CharField(required = False, max_length=13, min_length=10, widget=forms.TextInput(attrs={'placeholder': 'Enter ISBN number of the Book', 'size':40}))
    book_image_url = forms.URLField(required = False, max_length=200, widget=forms.URLInput(attrs={'placeholder': 'Enter URL of the Book Cover', 'size':40}))

    def clean_book_title(self):
        book_title = self.cleaned_data['book_title']

        return book_title

    def clean_book_author(self):
        book_author = self.cleaned_data['book_author']
        return book_author

    def clean_book_isbn(self):
        book_isbn = self.cleaned_data['book_isbn']
        return book_isbn
    
    def clean_book_url(self):
        book_image_url = self.cleaned_data['book_image_url']
        return book_image_url

    def clean(self):
        cleaned_data = super(SearchManualForm, self).clean()
        book_title = self.cleaned_data.get("book_title")
        book_author = self.cleaned_data.get("book_author")
        book_isbn = self.cleaned_data.get("book_isbn")
        book_image_url = self.cleaned_data.get("book_image_url")

        if book_title== '' and book_author=='' and book_isbn=='' and book_image_url=='':
            raise forms.ValidationError(_("Atleast one of the search fields must be filled out to perform the search."))

        if book_title== '' and book_author=='' and book_isbn=='' and book_image_url!='':
            raise forms.ValidationError(_("Cannot Perform Search only based on Image URL."))

        return cleaned_data

class JsonForm(MultipleForm):
    json_code = forms.CharField(widget=forms.Textarea(attrs={'rows':30, 'cols':60,'placeholder': 'Enter JSON code to search Digital/Audio Book'}))

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

class QueryForm(forms.Form):
    companies = Company.objects.all()
    company_list = ["None"]

    for company in companies:
        company_list.append(company.name)

    month = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Enter the Month Number e.g. January =1', 'size':28}))
    year = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Enter the Year', 'size':28}))
    company = forms.ChoiceField(required = False, choices= [(x, x)for x in company_list], help_text= 'Not Required')

    def clean_month(self):
        data = self.cleaned_data['month']

        if data>12 or data<1:
            raise ValidationError(_('Invalid Month Entered'))

        return data
    
    def clean_year(self):
        data = self.cleaned_data['year']

        if len(str(data))!= 4:
            raise ValidationError(_('Invalid Year Entered'))

        return data

    def clean_company(self):
        data = self.cleaned_data['company']
        return data