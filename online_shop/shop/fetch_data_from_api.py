import requests
from django.db import models
from .models import Author, Book  

# Replace with API key (if required)
API_KEY = ""

def fetch_and_save_books():
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": "fiction",  # Replace with search query
        "maxResults": 20,  # Adjust the number of books to fetch
        "key": API_KEY,  # Add API key here if needed
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "items" not in data:
        print("Error: No books found in the response.")
        return

    for item in data["items"]:
        volume_info = item["volumeInfo"]
        title = volume_info.get("title")
        authors = volume_info.get("authors")
        category = volume_info.get("categories", [""])[0]  # Handle potential missing category

        if not title or not authors:
            # Skip books with missing data
            continue

        # Create or get the Author(s)
        author_objects = []
        for author_name in authors:
            author, created = Author.objects.get_or_create(name=author_name)
            author_objects.append(author)

        # Create the Book
        book = Book.objects.create(
            title=title,
            category=category,
            # Add other book fields as needed, based on available data from the API
        )

        # Set the ManyToMany relationship between Book and Author
        book.authors.set(author_objects)

        print(f"Saved book: {title}")

if __name__ == "__main__":
    fetch_and_save_books() 
