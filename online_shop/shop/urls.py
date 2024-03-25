from django.urls import path
from .views import BookListView, BookDetailPageView, add_to_cart, remove_from_cart, view_cart, order_confirmation, wishlist, add_to_wishlist, remove_from_wishlist

app_name = 'shop' 

urlpatterns = [
    path('books/', BookListView.as_view(), name='book_list'),
    path('books/<int:pk>/', BookDetailPageView.as_view(), name='book_detail'),
    path('add_to_wishlist/<int:book_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:book_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/', wishlist, name='wishlist'),
    path('add-to-cart/<int:book_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:book_id>/', remove_from_cart, name='remove_from_cart'),
    path('view-cart/', view_cart, name='view_cart'),
    path('order_confirmation/', order_confirmation, name='order_confirmation'),
]
