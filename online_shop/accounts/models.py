from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    age = models.PositiveIntegerField(null=True)
    order_history = models.ManyToManyField('shop.Order', blank=True, related_name='custom_user_orders')
    shopping_cart = models.ManyToManyField('shop.Book', blank=True, related_name='custom_user_cart')
    wishlist = models.ManyToManyField('shop.Book', blank=True, related_name='custom_user_wishlist')


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.comment

class Rate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self) :
        return self.rating
