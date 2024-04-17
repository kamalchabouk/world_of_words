from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Book, Order, Payment #, OrderItem
from .forms import OrderForm
from django.db import transaction
from django.http import HttpResponseServerError
import requests
from django.http import JsonResponse
from django.forms.models import model_to_dict
from decimal import Decimal
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse
from django.utils import timezone
import json
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model

class BookListView(View):
    def get(self, request):
        all_books = Book.objects.all()  # Fetch all books from the database
        # featured_books = Book.objects.filter(featured=True)  # Assuming you have a field named 'featured'
        return render(
            request, "book_list.html", {"all_books": all_books}
        )  #'featured_books': featured_books})


@login_required
def add_to_wishlist(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    request.user.wishlist.add(book)
    return redirect("shop:wishlist")


@login_required
def remove_from_wishlist(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    request.user.wishlist.remove(book)
    return redirect("shop:wishlist")


@login_required
def wishlist(request):
    wishlist_books = request.user.wishlist.all()
    return render(request, "wishlist.html", {"wishlist_books": wishlist_books})


@login_required
def add_selected_to_cart(request, book_id):
    if request.method == "POST":
        book_ids = request.POST.getlist("books_to_add[]")

        if not book_ids:
            return HttpResponse("No books selected", status=400)

        cart = request.session.get("cart", {})

        for book_id in book_ids:
            book = get_object_or_404(Book, pk=book_id)
            cart_item = cart.get(str(book_id))

            if cart_item:
                cart_item["quantity"] += 1
            else:
                cart_item = {
                    "quantity": 1,
                    "price": str(book.price),
                }  
            cart[str(book_id)] = cart_item

           
            request.user.wishlist.remove(book)

        request.session["cart"] = cart
        return redirect("shop:view_cart")
    else:
        return HttpResponse("Method not allowed", status=405)


@login_required
def empty_cart(request):
    if request.method == "POST":
        request.session["cart"] = {}  # Set cart to an empty dictionary
        return redirect(
            "shop:view_cart"
        )  # Redirect to the cart view after emptying the cart

    return HttpResponseNotFound("Invalid request")  # Handle invalid requests


@login_required
def add_to_cart(request, book_id):
    User = get_user_model()
    book = get_object_or_404(Book, pk=book_id)
    cart = request.session.get("cart", {})

    # Check if the book is in the wishlist
    if book in request.user.wishlist.all():
        # Remove the book from the wishlist
        request.user.wishlist.remove(book)

    cart_item = cart.get(str(book_id))
    if cart_item:
        cart_item["quantity"] += 1
    else:
        cart_item = {
            "quantity": 1,
            "price": str(book.price),
        }  # Ensure price is a string
    cart[str(book_id)] = cart_item
    request.session["cart"] = cart

    # Add the book to the user's shopping cart
    user = request.user
    user.shopping_cart.add(book)
    user.save()

    next_page = request.GET.get("next", None)
    if next_page:
        return redirect(next_page)
    else:
        return redirect(reverse("shop:book_list"))

@login_required
def remove_from_cart(request, book_id):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        cart = request.session.get('cart', {})

        if book_id:
            cart = request.session.get('cart', {})
            if book_id in cart:
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

@login_required
def view_cart(request):
    cart = request.session.get("cart", {})
    cart_items = []
    total_price = 0

    if not cart:
        messages.info(request, "Your cart is empty.")
        #return redirect('shop:book_list')

    # Process cart items and calculate total price
    for book_id, item in cart.items():
        book = get_object_or_404(Book, pk=int(book_id))
        item_total = book.price * item["quantity"]
        cart_items.append({
            "pk": book.pk,
            "book_id": book_id,
            "title": book.title,
            "author": book.author,  # Assuming you have an author field
            "author_pk": book.author.pk,  # Assuming author has a primary key
            "price": str(book.price),
            "availability": book.availability,
            "quantity": item["quantity"],
            "item_total": str(item_total),
        })
        total_price += item_total

    # Consider passing cart items for pre-populating the order form (optional)
    order_form = OrderForm(cart_items=cart_items)

    return render(
        request,
        "view_cart.html",
        context={
            "cart_items": cart_items,
            "total_price": total_price,
            "order_form": order_form,
        },
    )

class BookDetailPageView(View):
    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        form = OrderForm(initial={"book": book})
        return render(request, "book_detail.html", {"book": book, "form": form})

    def post(self, request, book_id):
        if not request.user.is_authenticated:
            return redirect("login")
        book = get_object_or_404(Book, pk=book_id)
        if "add_to_cart" in request.POST:
            return add_to_cart(
                request, book_id=book_id
            )  # Call add_to_cart view function
        elif "add_to_wishlist" in request.POST:
            return add_to_wishlist(request, book_id=book_id)


class OrderView(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        cart_items = []
        total_price = 0

        if not cart:
            messages.error(request, "Your cart is empty. Please add items to your cart before checkout.")
            return redirect('shop:books')

        for book_id, item in cart.items():
            book = get_object_or_404(Book, pk=int(book_id))
            item_total = book.price * item['quantity']
            cart_items.append({'book': book, 'quantity': item['quantity'], 'item_total': item_total})
            total_price += item_total

        order_form = OrderForm(cart_items=cart_items)
        context = {'cart_items': cart_items, 'total_price': total_price, 'order_form': order_form}
        return render(request, 'view_cart.html', context)
    
    @transaction.atomic
    def post(self, request):

        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "Your cart is empty. Please add items to your cart before checkout.")
            return redirect('shop:view_cart')

        order_form = OrderForm(request.POST, cart_items=cart)
        orders = []
        if order_form.is_valid():
            total_quantity = 0
            total_price = 0
            orders = []
            payments = []
            for book_id, item in cart.items():
                book = get_object_or_404(Book, pk=int(book_id))
                total_quantity += item['quantity']
                total_price += item['quantity'] * book.price

                order = Order(
                    user=request.user,
                    book=book,
                    order_date=timezone.now(),
                    payment_type=order_form.cleaned_data.get('payment_type'),
                    order_status='Pending',
                    address=order_form.cleaned_data.get('address'),
                    quantity=item['quantity'],
                    amount=item['quantity'] * book.price,
                    paypal_address=order_form.cleaned_data.get('paypal_address'),
                    bank_name=order_form.cleaned_data.get('bank_name'),
                    account_number=order_form.cleaned_data.get('account_number'),
                    iban=order_form.cleaned_data.get('iban')
                )
                order.save()
                orders.append(order)


                payment = Payment(
                    order=order,
                    user=request.user,
                    book=book,
                    quantity=item['quantity'],
                    amount=item['quantity'] * book.price,
                    payment_type=order.payment_type,
                    status='Pending'
                )
                payment.save()
                payments.append(payment)
                
            for order in orders:

                book = order.book
                quantity = order.quantity
                book.quantity -= quantity
                if book.quantity <= 0:
                    try:
                        book.delete()
                    except Exception as e:
                        print(f"Error deleting book: {e}")
                        messages.error(request, f"Error deleting book: {e}")
                else:
                    book.save()

            del request.session['cart']
            print  
            return redirect('shop:thank_you')
        else:
            print("Form is not valid:", order_form.errors)  # Debugging
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
    # Retrieve the user's orders from the database
    user_orders = Order.objects.filter(user=request.user)

    context = {
        'user_orders': user_orders
    }
    return render(request, "thank_you.html", context)

def contacts(request):
    api_url = "http://127.0.0.1:5000/api/contacts/"
    response = requests.get(api_url)

    if response.status_code == 200:
        contacts = response.json()  # access JSON data
        return render(request, "contact.html", {"contacts": contacts})
    else:
        # Handle unsuccessful API request
        return render(request, "contact.html", {"contacts": []})


def contactdetails(request, contact_id):
    api_url = f"http://127.0.0.1:5000/api/contacts/{contact_id}/"
    response = requests.get(api_url)

    if response.status_code == 200:
        contact_details = (
            response.json()
        )  #  returns a single contact object
        return render(
            request, "contactdetails.html", {"contact_details": contact_details}
        )
    else:
        # Handle unsuccessful API request or contact not found
        return render(request, "contactdetails.html", {"contact_details": None})
    

def genres(request):
    api_url = "http://127.0.0.1:5000/api/genres/"
    response = requests.get(api_url)

    if response.status_code == 200:
        genres = response.json()  # access JSON data
        return render(request, "genres.html", {"genres": genres})
    else:
        # Handle unsuccessful API request
        return render(request, "genres.html", {"genres": []})


def genredetails(request, genre_id):
    api_url = f"http://127.0.0.1:5000/api/genres/{genre_id}/"
    response = requests.get(api_url)

    if response.status_code == 200:
        genre_details = (
            response.json()
        )  #  returns a single genre object
        return render(
            request, "genredetails.html", {"genre_details": genre_details}
        )
    else:
        # Handle unsuccessful API request or contact not found
        return render(request, "genredetails.html", {"genre_details": None})

def shop_home(request):
    return render(request, 'home.html')

def shop_genres(request):
    return render(request, 'genres.html')

class BookAsListView(View):
    def get(self, request):
        all_books = Book.objects.all()  # Fetch all books from the database
        # featured_books = Book.objects.filter(featured=True)  # Assuming you have a field named 'featured'
        return render(
            request, "books_as_list.html", {"all_books": all_books}
        )  #'featured_books': featured_books})


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
