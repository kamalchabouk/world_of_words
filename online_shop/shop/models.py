from django.db import models
from users.models import CustomUser  


class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    profile = models.TextField()
    book_list = models.ManyToManyField('Book', related_name='authors', blank=True)

class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    # Foreign keys
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  
    author_name = models.ForeignKey(Author, on_delete=models.CASCADE)
    
    # Other fields
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100)  
    quantity = models.IntegerField(default=1)
    publisher = models.CharField(max_length=100)
    publish_date = models.DateField()
    rating = models.IntegerField()
    availability = models.BooleanField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.ImageField(upload_to='book_pictures/', blank=True, null=True)

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    payment_type = models.CharField(max_length=100)
    order_status = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    delivery_date = models.DateTimeField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
