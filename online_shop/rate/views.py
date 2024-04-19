from django.shortcuts import render
from .forms import BookReviewForm
from shop.models import Book
from accounts.models import CustomUser

# Create your views here.
def add_review_book(request, pid):
    book = Book.objects.get(pk=pid)
    user = request.user
