from django.shortcuts import render
from shop.models import Book
from .forms import FilterForm
from django.db.models import Q

def filter_view(request):
    form = FilterForm(request.GET)
    items = []

    if form.is_valid():
        params = {}
        for field_name, value in form.cleaned_data.items():
            if value:
                params[field_name] = value

        if params:
            query = Q()
            # Filter by price range (if provided)
            if 'min_price' in params and 'max_price' in params:
                min_price = params['min_price']
                max_price = params['max_price']
                query = query & Q(price__gte=min_price, price__lte=max_price)
            # Filter by year range (if provided)
            if 'min_year' in params and 'max_year' in params:
                min_year = params['min_year']
                max_year = params['max_year']
                query = query & Q(publication_year__gte=min_year, publication_year__lte=max_year)
            # Filter by genre (if provided)
            if 'genre' in params:
                genre = params['genre']
                query = query & Q(genre__icontains=genre)

            items = Book.objects.filter(query)

    return render(request, 'filter.html', {'form': form, 'items': items})