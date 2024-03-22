from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Book, Order, Payment
from .forms import OrderForm
from django.db import transaction
import requests
from django.http import JsonResponse

class BookListView(View):
    def get(self, request):
        products = Book.objects.all()  # Fetch all products from the database
        return render(request, 'book_list.html', {'products': products})

def add_to_wishlist(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    request.user.wishlist.add(book)
    return redirect('wishlist')

def remove_from_wishlist(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    request.user.wishlist.remove(book)
    return redirect('wishlist')

def wishlist(request):
    wishlist_books = request.user.wishlist.all()
    return render(request, 'wishlist.html', {'wishlist_books': wishlist_books})  


def add_to_cart(request, book_id):
    book = Book.objects.get(id=book_id)
    cart = request.session.get('cart', {})
    cart_item = cart.get(str(book_id))
    if cart_item:
        cart_item['quantity'] += 1
    else:
        cart_item = {'quantity': 1}
    cart[str(book_id)] = cart_item
    request.session['cart'] = cart
    return redirect('cart')

def remove_from_cart(request, book_id):
    cart = request.session.get('cart', {})
    if str(book_id) in cart:
        del cart[str(book_id)]
        request.session['cart'] = cart
    return redirect('cart')

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    for book_id, item in cart.items():
        book = Book.objects.get(id=int(book_id))
        item_total = book.price * item['quantity']
        cart_items.append({'book': book, 'quantity': item['quantity'], 'item_total': item_total})
        total_price += item_total
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

class BookDetailPageView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Book, pk=product_id)
        form = OrderForm(initial={'book': product})  
        return render(request, 'detailed_product_page.html', {'product': product, 'form': form})
    
    @transaction.atomic
    def post(self, request, product_id):
        if not request.user.is_authenticated:
            return redirect('login') 
        
        product = get_object_or_404(Book, pk=product_id)
        profile = request.user.profile

        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                order.book = product
                order.profile = profile 
                order.save()

                # Update book availability or delete book if needed
                quantity = form.cleaned_data.get('quantity', 1)
                product.availability -= quantity
                if product.availability <= 0:
                    try:
                        product.delete()
                    except Exception as e:
                        print(f"Error deleting product: {e}")
                else:
                    product.save()

                # Create payment record
                payment = Payment.objects.create(
                order=order,
                user=request.user,
                book=product,
                quantity=quantity,
                amount=form.cleaned_data.get('amount'),
                payment_type=form.cleaned_data.get('payment_type'),
                status='Pending'  # Set initial status as Pending
            )


                # Redirect to payment page
                return redirect('order_confirmation') 
        else:
            form = OrderForm(initial={'book': product}) 

        # Form is not valid, re-render the page with the form and product
        return render(request, 'detailed_product_page.html', {'product': product, 'form': form})





def order_confirmation(request):
    return render(request, 'thank_you.html')


def search_books(request):
    query = request.GET.get('q', '')  # Get the search query from the request
    pages = request.GET.get('pages', '1')  # Get the number of pages to fetch (default is 1)
    
    # Make a GET request to the /search endpoint to search for books
    endpoint = f"http://barnesandnobles.herokuapp.com/api/search/{query}/{pages}"
    response = requests.get(endpoint)

    if response.status_code == 200:
        data = response.json()
        
        for book_data in data:
            # Extract book information from the API response
            title = book_data.get('title', '')
            author = book_data.get('author', '')
            price_str = book_data.get('price', '').replace('$', '')  # Remove '$' sign
            price = float(price_str) if price_str else 0.0  # Convert price to float
            
            
            # Create Book object
            Book.objects.create(
                title=title,
                author=author,
                price=price,
                
            )
        
        return JsonResponse({'message': 'Books saved successfully'})
    else:
        return JsonResponse({'error': 'Failed to fetch data from the API'}, status=500)
