from django import forms  
from shop.models import Book

class FilterForm(forms.Form):
    min_price = forms.DecimalField(required=False, label='Minimum Price')
    max_price = forms.DecimalField(required=False, label='Maximum Price')
    min_pages = forms.IntegerField(required=False, label='Minimum Pages')
    max_pages = forms.IntegerField(required=False, label='Maximum Pages')
    genre = forms.CharField(required=False, label='Genre')

    class Meta:
        model = Book
        fields = ['min_price', 'max_price',  'min_pages', 'max_pages', 'genre']