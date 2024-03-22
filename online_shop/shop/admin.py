from django.contrib import admin
from .models import Book, Author, Payment, Order

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Payment)
admin.site.register(Order)
