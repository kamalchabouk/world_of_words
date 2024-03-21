from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    userid = models.CharField(max_length=50, unique=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    age = models.PositiveIntegerField()
    order_history = models.ManyToManyField('Order', blank=True)
    shopping_cart = models.ManyToManyField('Product', blank=True)
    wishlist = models.ManyToManyField('Product', blank=True)

