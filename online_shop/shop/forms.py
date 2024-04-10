from django import forms
from django.utils import timezone
from .models import Order

class OrderForm(forms.ModelForm):
    payment_type = forms.ChoiceField(choices=[
        ('paypal', 'Paypal'),
        ('banktransfer', 'Bank Transfer')
    ], widget=forms.RadioSelect)

    class Meta:
        model = Order
        fields = ['payment_type', 'address', 'paypal_address', 'bank_name', 'account_number', 'iban']

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['delivery_date'] = timezone.now() + timezone.timedelta(days=7)
        return cleaned_data

    def __init__(self, *args, **kwargs):
        cart_items = kwargs.pop('cart_items', None)
        super(OrderForm, self).__init__(*args, **kwargs)

        self.fields['payment_type'].widget.attrs['onchange'] = 'toggleFields(this.value)'
        self.fields['paypal_address'].widget.attrs['class'] = 'paypal-field'
        self.fields['bank_name'].widget.attrs['class'] = 'bank-transfer-field'
        self.fields['account_number'].widget.attrs['class'] = 'bank-transfer-field'
        self.fields['iban'].widget.attrs['class'] = 'bank-transfer-field'

