from django import forms
from django.utils import timezone
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['book', 'author', 'order_date', 'payment_type', 'order_status', 'address', 'quantity', 'delivery_date']
        widgets = {
            'order_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
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
