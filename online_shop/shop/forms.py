from django import forms
from django.utils import timezone
from .models import Order, Book, Author

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['book', 'author', 'payment_type', 'address', 'quantity', 'delivery_date']
        widgets = {
            'delivery_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'address': forms.TextInput(attrs={'readonly': 'readonly'})  # Make the address field read-only
        }

    def __init__(self, *args, **kwargs):
        # Retrieve the user's address from the database
        user_address = kwargs.pop('user_address', None)
        super(OrderForm, self).__init__(*args, **kwargs)

        # Prepopulate the address field with the user's address
        if user_address:
            self.fields['address'].initial = user_address

        # Set the default delivery date to 7 days from ordering
        if 'order_date' in self.initial:
            order_date = self.initial['order_date']
            default_delivery_date = order_date + timezone.timedelta(days=7)
            self.fields['delivery_date'].initial = default_delivery_date

        # Prepopulate the book and author fields with initial data
        if 'book' in self.initial:
            self.fields['book'].queryset = Book.objects.filter(pk=self.initial['book'].pk)
        if 'author' in self.initial:
            self.fields['author'].queryset = Author.objects.filter(pk=self.initial['author'].pk)
