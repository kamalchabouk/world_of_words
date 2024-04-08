from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    age = models.PositiveIntegerField(blank=True, null=True)
    order_history = models.ManyToManyField('shop.Order', blank=True, related_name='custom_user_orders')
    shopping_cart = models.ManyToManyField('shop.Book', blank=True, related_name='custom_user_cart')
    wishlist = models.ManyToManyField('shop.Book', blank=True, related_name='custom_user_wishlist')


