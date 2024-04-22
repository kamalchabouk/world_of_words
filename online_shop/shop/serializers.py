from rest_framework import serializers
from .models import Book,Payment,Order,Author

class BookSerializer(serializers.ModelSerializer):
  class Meta:
    model = Book
    fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Payment
    fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
  class Meta:
    model = Order
    fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Author