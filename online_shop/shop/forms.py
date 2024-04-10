from django import forms
from django.utils import timezone
from .models import Order, Book, Author

class OrderForm(forms.ModelForm):
    payment_type = forms.ChoiceField(choices=[
        ('paypal', 'Paypal'),
        ('banktransfer', 'Bank Transfer')
    ])

    class Meta:
        model = Order
        fields = ['payment_type', 'address']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        cart_items = kwargs.pop('cart_items', None)
        super(OrderForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['address'].initial = user.address

        if cart_items:
            for index, cart_item in enumerate(cart_items):
                book = cart_item['book']
                author = book.author
                # Add hidden fields for book and author
                self.fields[f'book_{index}'] = forms.CharField(initial=book.title, widget=forms.HiddenInput())
                self.fields[f'author_{index}'] = forms.CharField(initial=author.pk, widget=forms.HiddenInput())  # Use author.pk for the author_id

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['delivery_date'] = timezone.now() + timezone.timedelta(days=7)  # Set delivery date 7 days from now
        return cleaned_data
