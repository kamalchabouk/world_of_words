# test.py
import os
import django

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_shop.settings')
django.setup()

from shop.models import Book

def check_book_existence(book_id):
    try:
        book = Book.objects.get(pk=book_id)
        return True  # Book with the given ID exists
    except Book.DoesNotExist:
        return False  # Book with the given ID does not exist

# Example usage:
book_id_to_check = 5  # Replace 1 with the ID you want to check
if check_book_existence(book_id_to_check):
    print("Book exists in the database.")
else:
    print("Book does not exist in the database.")
