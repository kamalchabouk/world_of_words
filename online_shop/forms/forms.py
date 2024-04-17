from django import forms
from shop.models import Book 
class AddBookForm(forms.Form):
    author = forms.CharField(max_length=255, required=False)
    title = forms.CharField(widget=forms.Textarea, required=False)
    pages = forms.IntegerField(required=False)
    year = forms.IntegerField(required=False)
    genre = forms.CharField(max_length=50, required=False)
    quantity = forms.IntegerField(required=False)
    availability = forms.BooleanField(required=False, initial=True)
    language = forms.CharField(max_length=50, required=False)
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    picture = forms.ImageField(required=False)


 # Assuming your book model is in the same app

class UpdateBookForm(forms.ModelForm):
    class Meta:
        model = Book  
        fields = ['title', 'author',  'price','language','pages','year','genre', 'availability', 'picture']  # Fields to edit

    def clean_title(self):
        title = self.cleaned_data['title']

        return title