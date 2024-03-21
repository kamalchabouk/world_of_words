
from django import forms

class FilterForm(forms.Form):
    min_price = forms.DecimalField(required=False)
    max_price = forms.DecimalField(required=False)
    author = forms.CharField(required=False)
    title = forms.CharField(required=False)