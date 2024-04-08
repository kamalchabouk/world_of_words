from django.urls import reverse_lazy
from django.shortcuts import render, redirect
import requests
from django.http import HttpResponse, HttpResponseServerError
from django.views.generic.edit import FormView,UpdateView
from django.views import View
from .forms import AddBookForm

from django.views.generic.edit import FormView,DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseServerError
from .forms import AddBookForm
from shop.models import Book

class AddBookView(FormView):
    template_name = 'add_new_book.html'
    form_class = AddBookForm
    success_url = reverse_lazy('shop:book_list')

    def form_valid(self, form):
        # Extract form data
        author = form.cleaned_data['author']
        title = form.cleaned_data['title']
        pages = form.cleaned_data['pages']
        year = form.cleaned_data['year']
        genre = form.cleaned_data['genre']
        quantity = form.cleaned_data['quantity']
        availability = form.cleaned_data['availability']
        language = form.cleaned_data['language']
        price = form.cleaned_data['price']
        picture = form.cleaned_data['picture']

        # Save the form data to the database
        try:
            Book.objects.create(
                author=author,
                title=title,
                pages=pages,
                year=year,
                genre=genre,
                quantity=quantity,
                availability=availability,
                language=language,
                price=price,
                picture=picture
            )
        except HttpResponseServerError as e:
            form.add_error(None, 'An error occurred while adding the book: {}'.format(str(e)))
            return self.form_invalid(form)

        return super().form_valid(form)

class EditBookView(UpdateView):
    model = Book
    form_class = AddBookForm
    template_name = 'edit_book.html'
    success_url = reverse_lazy('shop:book_detail')


class BookDeleteView(DeleteView):
    model = Book
    success_url = reverse_lazy('shop:book_list')  # Redirect URL after successful deletion
    template_name = 'delete_book.html' 