from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Book, Order, Payment, OrderItem
from .forms import OrderForm
from django.db import transaction
import requests
from django.http import JsonResponse
from django.forms.models import model_to_dict
from decimal import Decimal
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse

class BookListView(View):
    def get(self, request):
        all_books = Book.objects.all()  # Fetch all books from the database
        #featured_books = Book.objects.filter(featured=True)  # Assuming you have a field named 'featured'
        return render(request, 'book_list.html', {'all_books': all_books})#'featured_books': featured_books})

def add_to_wishlist(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    request.user.wishlist.add(book)
    return redirect('shop:wishlist')

def remove_from_wishlist(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    request.user.wishlist.remove(book)
    return redirect('shop:wishlist')

def wishlist(request):
    wishlist_books = request.user.wishlist.all()
    return render(request, 'wishlist.html', {'wishlist_books': wishlist_books})  



def empty_cart(request):
    if request.method == 'POST':
        request.session['cart'] = {}  # Set cart to an empty dictionary
        return redirect('shop:view_cart')  # Redirect to the cart view after emptying the cart

    return HttpResponseNotFound('Invalid request')  # Handle invalid requests

def add_to_cart(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    cart = request.session.get('cart', {})
    cart_item = cart.get(str(book_id))
    if cart_item:
        cart_item['quantity'] += 1
    else:
        cart_item = {'quantity': 1, 'price': str(book.price)}  # Ensure price is a string
    cart[str(book_id)] = cart_item
    request.session['cart'] = cart
    next_page = request.GET.get('next', None)
    if next_page:
        return redirect(next_page)
    else:
        return redirect(reverse('shop:book_list'))

def remove_from_cart(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        cart = request.session.get('cart', {})

        if book_id and book_id in cart:
            del cart[book_id]

            # Recalculate total price after removing the item
            total_price = 0
            for item_id, item_data in cart.items():
                # Convert item price to float before adding
                item_total = float(item_data['quantity']) * float(item_data['price'])
                total_price += item_total

            request.session['cart'] = cart

            # Redirect to the view_cart page after successful removal
            return redirect('shop:view_cart')

    return HttpResponseNotFound('Invalid request')



def view_cart(request, context=None):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = context.get('total_price', None) if context else None
    order_form = None  # Ensure order_form is always assigned

    if not total_price:
        total_price = 0
        for book_id, item in cart.items():
            book = get_object_or_404(Book, pk=int(book_id))
            item_total = book.price * item['quantity']
            cart_items.append({
                'pk': book.pk,
                'title': book.title,
                'author': book.author,#.name if book.author else "",  # Add author information
                'author_pk': book.author.pk,                 
                'price': str(book.price),
                'availability': book.availability,
                'quantity': item['quantity'],
                'item_total': str(item_total)
            })
            total_price += item_total
        order_form = OrderForm()  # Assign order_form when calculating total_price

    return render(request, 'view_cart.html', context={'cart_items': cart_items, 'total_price': total_price, 'order_form': order_form})

# def remove_from_cart(request):
#     if request.method == 'POST':
#         book_id = request.POST.get('book_id')
#         cart = request.session.get('cart', {})  # Get current cart

#         if book_id and book_id in cart:
#             del cart[book_id]  # Remove entire cart item entry

#             # Recalculate total price after removing the item
#             total_price = 0
#             for item_id, item_data in cart.items():
#                 # Ensure price is numerical before multiplication
#                 if not isinstance(item_data['price'], (int, float)):
#                     item_data['price'] = float(item_data['price'])  # Convert to float if necessary
#                 total_price += item_data['quantity'] * item_data['price']

#             request.session['cart'] = cart  # Update session cart
#             return redirect('shop:view_cart')  # Redirect to cart view with recalculated price

#     return HttpResponseNotFound('Invalid request') 



# # Added line for inspection
# def view_cart(request):
#     cart = request.session.get('cart', {})
#     cart_items = []
#     total_price = 0
#     for book_id, item in cart.items():
#         book = Book.objects.get(pk=int(book_id))
#         item_total = book.price * item['quantity']
#         cart_items.append({
#             'pk': book.pk,  # Use book.pk instead of book.id
#             'title': book.title,
#             'author': book.author.name if book.author else "",  # Optional: Include author if available
#             'price': str(book.price),
#             'availability': book.availability,
#             'quantity': item['quantity'],
#             'item_total': str(item_total)
#         })
#         total_price += item_total
#     total_price = str(total_price)  # Convert to string
#     context = {'cart_items': cart_items, 'total_price': total_price}

#     return render(request, 'view_cart.html', context)


class BookDetailPageView(View):
    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        form = OrderForm(initial={'book': book})  
        return render(request, 'book_detail.html', {'book': book, 'form': form})
    
    def post(self, request, book_id):
        if not request.user.is_authenticated:
            return redirect('login') 
        book = get_object_or_404(Book, pk=book_id)
        if 'add_to_cart' in request.POST:
            return add_to_cart(request, book_id=book_id)  # Call add_to_cart view function
        elif 'add_to_wishlist' in request.POST:
            return add_to_wishlist(request, book_id=book_id)  

class OrderView(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        cart_items = []
        total_price = 0

        for book_id, item in cart.items():
            book = get_object_or_404(Book, pk=int(book_id))
            item_total = book.price * item['quantity']
            cart_items.append({'book': book, 'quantity': item['quantity'], 'item_total': item_total})
            total_price += item_total

        order_form = OrderForm(cart_items=cart_items)
        context = {'cart_items': cart_items, 'total_price': total_price, 'order_form': order_form}
        return render(request, 'thank_you.html', context)

    
    def post(self, request):
        cart = request.session.get('cart', {})
        order_form = OrderForm(request.POST)

        if order_form.is_valid():
            order = order_form.save(commit=False)
            # Calculate total quantity and total price before saving the order
            total_quantity = 0  # Initialize total_quantity here
            total_price = 0
            if cart:
                for book_id, item in cart.items():
                    total_quantity += item['quantity']
                    item_price = Decimal(item['price'])  # Ensure price is a decimal
                    total_price += item['quantity'] * item_price

            # Set order quantity and amount before first save
            order.quantity = total_quantity
            order.amount = total_price
            order.user = request.user
            order.save()  # First save with quantity and amount

            # Check if cart is empty before processing
            if cart:
                # Print book details for verification (optional)
                for book_id, item in cart.items():
                    print(f"Book ID: {book_id}, Quantity: {item['quantity']}, Price: {item['price']}")

            # Iterate through cart items and create OrderItem objects
                for book_id, item in cart.items():
                    order_item = OrderItem.objects.create(
                        order=order,
                        book_id=book_id,
                        quantity=item['quantity']
                    )

                    # Ensure price is a decimal before multiplication
                    item_price = Decimal(item_price)  # Assuming price is stored as a string
                    total_price += item['quantity'] * item_price

            else:
                # Handle empty cart scenario (e.g., display an error message)
                return render(request, 'view_cart.html', {'error': 'Your cart is empty.'})

            # Update order with total price only if cart is not empty
            if total_price > 0:
                order.amount = total_price
                order.save()
            else:
                # In case total_price becomes 0 even with non-empty cart (due to calculation errors)
                pass 

            for book_id, item in cart.items():
                #book = get_object_or_404(Book, pk=int(book_id))
                author_id = request.POST.get(f'author_pk_{book_id}')
                payment = Payment.objects.create(
                    order=order,
                    user=request.user,
                    book=book,
                    quantity=item['quantity'],
                    amount=book.price * item['quantity'],
                    payment_type=order_form.cleaned_data.get('payment_type'),
                    status='Pending'
                )

                # Update book availability or delete book if needed
                quantity = item['quantity']
                book.availability -= quantity
                if book.availability <= 0:
                    try:
                        book.delete()
                    except Exception as e:
                        print(f"Error deleting book: {e}")
                else:
                    book.save()

            del request.session['cart']
            return redirect('shop:thank_you')  # Redirect to thank you page after successful order
        else:
            cart_items = []
            total_price = 0

            for book_id, item in cart.items():
                book = get_object_or_404(Book, pk=int(book_id))
                item_total = book.price * item['quantity']
                cart_items.append({'book': book, 'quantity': item['quantity'], 'item_total': item_total})
                total_price += item_total

            context = {'cart_items': cart_items, 'total_price': total_price, 'order_form': order_form}
            return render(request, 'view_cart.html', context)

def order_confirmation(request):
    return render(request, 'thank_you.html')


# def search_books(request):
#     query = request.GET.get('q', '')  # Get the search query from the request
#     pages = request.GET.get('pages', '1')  # Get the number of pages to fetch (default is 1)
    
#     # Make a GET request to the /search endpoint to search for books
#     endpoint = f"http://barnesandnobles.herokuapp.com/api/search/{query}/{pages}"
#     response = requests.get(endpoint)

#     if response.status_code == 200:
#         data = response.json()
        
#         for book_data in data:
#             # Extract book information from the API response
#             title = book_data.get('title', '')
#             author = book_data.get('author', '')
#             price_str = book_data.get('price', '').replace('$', '')  # Remove '$' sign
#             price = float(price_str) if price_str else 0.0  # Convert price to float
            
            
#             # Create Book object
#             Book.objects.create(
#                 title=title,
#                 author=author,
#                 price=price,
                
#             )
        
#         return JsonResponse({'message': 'Books saved successfully'})
#     else:
#         return JsonResponse({'error': 'Failed to fetch data from the API'}, status=500)
