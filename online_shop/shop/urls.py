from django.urls import path
from .views import BookListView, BookDetailPageView, BookAsListView, genres, genredetails, shop_home, contacts, contactdetails, add_to_cart, add_selected_to_cart, remove_from_cart, view_cart, empty_cart, order_confirmation, wishlist, add_to_wishlist, remove_from_wishlist, OrderView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'shop' 

urlpatterns = [
    path('books/', BookListView.as_view(), name='book_list'),
    path('book-list/', BookAsListView.as_view(), name='books_as_list'),
    path('books/<int:book_id>/', BookDetailPageView.as_view(), name='book_detail'),
    path('view-cart/', view_cart, name='view_cart'),
    path('add_to_wishlist/<int:book_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:book_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/', wishlist, name='wishlist'),
    path('add-selected-to-cart/<int:book_id>/', add_selected_to_cart, name='add_selected_to_cart'),
    path('add-to-cart/<int:book_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:book_id>/', remove_from_cart, name='remove_from_cart'),
    path('empty-cart/', empty_cart, name='empty_cart'), 
    path('checkout/', OrderView.as_view(), name='checkout'),    
    path('thank_you/', order_confirmation, name='thank_you'),
    path('contact/', contacts, name='contact'),
    path('contact_details/<int:contact_id>/', contactdetails, name='contact_details'),
    path('',shop_home, name='home' ),
    #path('genres/', shop_genres, name='genres'),
    path('genres/', genres, name='genres'),
    path('genre_details/<int:genre_id>/', genredetails, name='genre_details'),

]

