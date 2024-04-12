from django.test import TestCase, Client
from django.urls import reverse
from .models import Book, Order, Payment
from accounts.models import CustomUser 
from django.contrib.auth import get_user_model
from django.utils import timezone
from unittest.mock import patch
from shop.models import Book, Author, Order, Payment
from .views import add_to_wishlist, remove_from_wishlist, wishlist


CustomUser = get_user_model()

class ShopViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create(username='test_user', password='test_password')
        self.author = Author.objects.create(name='Test Author')  # Create a test author
        self.book = Book.objects.create(title='Test Book', price=10, author=self.author)  # Create a test book

    @patch('shop.models.Book.picture')
    def test_book_list_view(self, mock_picture):
        # Mock the behavior of the ImageField
        mock_picture.return_value = None
        
        response = self.client.get(reverse("shop:book_list"))
        self.assertEqual(response.status_code, 200)

    def test_view_cart_view(self):
        # Add the book to the cart
        self.client.force_login(self.user)
        self.client.session['cart'] = {str(self.book.pk): {"quantity": 1}}
        self.client.session.save()
        response = self.client.get(reverse("shop:view_cart"))
        self.assertEqual(response.status_code, 200)


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
        expected_books = [book1.title, book2.title]
        actual_books = list(response.context['wishlist_books'].values_list('title', flat=True))
        self.assertListEqual(sorted(expected_books), sorted(actual_books))

class OrderViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='12345')
        self.author = Author.objects.create(name='Test Author')  # Create a dummy author
        self.book = Book.objects.create(title='Test Book', price=10, author=self.author)  # Associate the author with the book


    def test_get_order_view(self):
        # Login the user
        self.client.force_login(self.user)
        
        # Add book to the cart
        session = self.client.session
        session['cart'] = {str(self.book.pk): {'quantity': 1}}
        session.save()

        # Make a GET request to the order view
        response = self.client.get(reverse('shop:view_cart'))

        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Check if the context contains the order form
        self.assertIn('order_form', response.context)


class APITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='12345')

    @patch('requests.get')
    def test_contacts(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{'id': 1, 'name': 'John'}, {'id': 2, 'name': 'Alice'}]

        response = self.client.get(reverse('shop:contact'))
        self.assertEqual(response.status_code, 200)

    @patch('requests.get')
    def test_contactdetails(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'id': 1, 'name': 'John'}

        response = self.client.get(reverse('shop:contact_details', kwargs={'contact_id': 1}))
        self.assertEqual(response.status_code, 200)

    @patch('requests.get')
    def test_genres(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{'id': 1, 'name': 'Fiction'}, {'id': 2, 'name': 'Thriller'}]

        response = self.client.get(reverse('shop:genres'))
        self.assertEqual(response.status_code, 200)

    @patch('requests.get')
    def test_genredetails(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'id': 1, 'name': 'Fiction'}

        response = self.client.get(reverse('shop:genre_details', kwargs={'genre_id': 1}))
        self.assertEqual(response.status_code, 200)
