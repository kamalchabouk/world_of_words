from django.test import TestCase, Client
from django.urls import reverse
from .models import Book, Order, Payment
from accounts.models import CustomUser 
from django.contrib.auth import get_user_model
from unittest.mock import patch
from shop.models import Book, Author
from .views import add_to_wishlist, remove_from_wishlist, wishlist

CustomUser = get_user_model()

class ShopViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    # def test_book_list_view(self):
    #     response = self.client.get(reverse("shop:book_list"))
    #     self.assertEqual(response.status_code, 200)
    #     # Add more assertions as needed

    # def test_add_to_cart_view(self):
    #     user = CustomUser.objects.create(username="test_user")  # Use CustomUser instead of User
    #     author = Author.objects.create(name="Test Author")  # Create a test author
    #     book = Book.objects.create(title="Test Book", price=10, author=author)  # Assign the test author to the book
    #     self.client.force_login(user)
    #     book.save()  # Save the book to the database
    #     response = self.client.get(reverse("shop:add_to_cart", kwargs={"book_id": book.book_id}))  # Access book_id instead of id
    #     self.assertEqual(response.status_code, 302)

class WishlistViewsTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='test_user', password='test_password')
        self.author = Author.objects.create(name='Test Author')  # Create a test author
        self.book = Book.objects.create(title='Test Book', price=10, author=self.author)  # Create a test book
    
    @patch('shop.models.Book.picture')
    def test_add_to_wishlist_view(self, mock_picture):
        # Mock the behavior of the ImageField
        mock_picture.return_value = None
        
        # Login the user
        self.client.force_login(self.user)
        
        # Make a POST request to add the book to the wishlist
        response = self.client.post(reverse("shop:add_to_wishlist", kwargs={"book_id": self.book.pk}))
        
        # Check if the response is a redirect (status code 302)
        self.assertEqual(response.status_code, 302)
        
        # Check if the book is in the user's wishlist
        self.assertTrue(self.user.wishlist.filter(pk=self.book.pk).exists())

    @patch('shop.models.Book.picture')
    def test_remove_from_wishlist_view(self, mock_picture):
        # Mock the behavior of the ImageField
        mock_picture.return_value = None
        
        # Add the test book to the wishlist
        self.user.wishlist.add(self.book)
        
        # Login the user
        self.client.force_login(self.user)
        
        # Make a POST request to remove the book from the wishlist
        response = self.client.post(reverse("shop:remove_from_wishlist", kwargs={"book_id": self.book.pk}))
        
        # Check if the response is a redirect (status code 302)
        self.assertEqual(response.status_code, 302)
        
        # Check if the book is removed from the user's wishlist
        self.assertFalse(self.user.wishlist.filter(pk=self.book.pk).exists())

    @patch('shop.models.Book.picture')
    def test_wishlist_view(self, mock_picture):
        # Mock the behavior of the ImageField
        mock_picture.return_value = None
        
        # Create additional test books with the existing author
        book1 = Book.objects.create(title="Test Book 1", price=10, author=self.author)
        book2 = Book.objects.create(title="Test Book 2", price=20, author=self.author)
        
        # Add additional test books to the wishlist
        self.user.wishlist.add(book1, book2)
        
        # Login the user
        self.client.force_login(self.user)
        
        # Get the wishlist page
        response = self.client.get(reverse("shop:wishlist"))
        
        # Check if the response is successful (status code 200)
        self.assertEqual(response.status_code, 200)
        
        # Check if the context contains the correct books
        self.assertQuerysetEqual(response.context['wishlist_books'], [repr(book1), repr(book2)])
