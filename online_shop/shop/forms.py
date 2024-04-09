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
        user = kwargs.pop('user', None)  # Get user from kwargs
        cart_items = kwargs.pop('cart_items', None)  # Get cart items from kwargs
        super(OrderForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['address'].initial = user.address  # Pre-fill address

        # Dynamically add form fields for each book and author in the cart
        if cart_items:
            for index, cart_item in enumerate(cart_items):
                # Add hidden fields for book and author
                book = Book.objects.get(pk=cart_item['book_id'])
                author = Author.objects.get(pk=cart_item['author_id'])
                self.fields[f'book_{index}'] = forms.CharField(initial=book.title, widget=forms.HiddenInput())
                self.fields[f'author_{index}'] = forms.CharField(initial=author.name, widget=forms.HiddenInput())

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['delivery_date'] = timezone.now() + timezone.timedelta(days=7)  # Set delivery date 7 days from now
        return cleaned_data
