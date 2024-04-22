import json
from .models import Book, Author
# Read the JSON file
import os 
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "online_shop.settings")
django.setup()

with open('shop/books.json', 'r') as f:
    books_data = json.load(f)

# Iterate over the book data
for book_data in books_data:
    # Assuming 'author' key exists in each book data
    author_name = book_data['author']
    author, created = Author.objects.get_or_create(name=author_name)

    # Create a book instance
    book = Book(
        author=author,
        title=book_data['title'],
        pages=book_data['pages'],
        year=book_data['year'],
        genre=book_data.get('genre'),  # Handle missing keys gracefully
        quantity=book_data.get('quantity'),
        availability=book_data.get('availability', True),
        language=book_data['language'],
        price=book_data.get('price'),
        picture=book_data['imageLink'], 
    )

    # Save the book instance
    book.save()
