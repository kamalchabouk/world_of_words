from django.shortcuts import get_object_or_404
from .models import Book, Author
from users.models import CustomUser


books_data = [
    {
        "category": "Fiction (Sci-Fi)",
        "title": "The Hitchhiker's Guide to the Galaxy",
        "author_name": "Douglas Adams", 
        "publisher": "Pan Books",
        "publish_date": "1979-10-04",
        "rating": 4.2,
        "availability": True,
        "price": 10.99,
        "picture": 'media/hitchhikersguide.jpg'
    },
    {
        "category": "Fiction (Fantasy)",
        "title": "A Game of Thrones",
        "author_name": "George R. R. Martin",  
        "publisher": "Bantam Books",
        "publish_date": "1996-08-01",
        "rating": 4.4,
        "availability": True,
        "price": 14.99,
        "picture": 'media/gameofthrones.jpg'
    },
    {
        "category": "Fiction (Mystery)",
        "title": "And Then There Were None",
        "author_name": "Agatha Christie",  
        "publisher": "HarperCollins",
        "publish_date": 1939,
        "rating": 4.3,
        "availability": True,
        "price": 8.99,
        "picture": 'media/andthen.jpeg'
    },
    {
        "category": "Non-Fiction (Biography)",
        "title": "I Am Malala: The Girl Who Stood Up for Education and Was Shot by the Taliban",
        "author_name": "Malala Yousafzai",  
        "publisher": "Little, Brown and Company",
        "publish_date": 2013,
        "rating": 4.6,
        "availability": True,
        "price": 12.99,
        "picture": 'media/huckleberry.jpg'
    },
    {
        "category": "Fiction (Classic)",
        "title": "The Adventures of Huckleberry Finn",
        "author_name": "Mark Twain"
        "publisher": "Various",
        "publish_date": 1885,
        "rating": 4.0,
        "availability": True,
        "price": 7.50,
        "picture": 'media/huckleberry.jpg'
    },
   
    {
        "category": "Non-Fiction (History)",
        "title": "A Short History of Nearly Everything",
        "author_name": "Bill Bryson", 
        "publisher": "Doubleday",
        "publish_date": 2003,
        "rating": 4.5,
        "availability": True,
        "price": 16.99,
        "picture": 'media/ashortstory.jpg'
    },
    {
        "category": "Fiction (Historical Fiction)",
        "title": "The Pillars of the Earth",
        "author_name": "Ken Follett",  
        "publisher": "Summit Books",
        "publish_date": 1989,
        "rating": 4.2,
        "availability": True,
        "price": 15.99,
        "picture": 'media/thepillars.jpg'
    },
    {
        "category": "Fiction (Romance)",
        "title": "Pride and Prejudice",
        "author_name": "Jane Austen", 
        "publisher": "Various",
        "publish_date": 1813,
        "rating": 4.2,
        "availability": True,
        "price": 9.99,
        "picture": 'media/prideandprejudice.jpg'
    },{
        'title': 'Harry Potter and the Sorcerer\'s Stone',
        'author_name': 'J.K. Rowling',
        'price': 12.99,
        'publisher': 'Scholastic Inc.',
        'publish_date': '1997-06-26',
        'rating': 4.5,
        'availability': True,
        'picture': 'media/harrypottersorcerer.jpg'
    },
    {
        'title': 'Harry Potter and the Chamber of Secrets',
        'author_name': 'J.K. Rowling',
        'price': 14.99,
        'publisher': 'Scholastic Inc.',
        'publish_date': '1998-07-02',
        'rating': 4.6,
        'availability': True,
        'picture': 'media/harrypotterchamber.jpg'
    },
    {
        'title': 'Harry Potter and the Prisoner of Azkaban',
        'author_name': 'J.K. Rowling',
        'price': 16.99,
        'publisher': 'Scholastic Inc.',
        'publish_date': '1999-09-08',
        'rating': 4.7,
        'availability': True,
        'picture': 'media/harrypotterazkaban.jpg'
    },
    {
        'title': 'The Fellowship of the Ring',
        'author_name': 'J.R.R. Tolkien',
        'price': 11.99,
        'publisher': 'Houghton Mifflin',
        'publish_date': '1954-07-29',
        'rating': 4.8,
        'availability': True,
        'picture': 'media/fellowshipofthering.jpg'
    },
    {
        'title': 'The Two Towers',
        'author_name': 'J.R.R. Tolkien',
        'price': 13.99,
        'publisher': 'Houghton Mifflin',
        'publish_date': '1954-11-11',
        'rating': 4.9,
        'availability': True,
        'picture': 'media/thetwotowers.jpg'
    },
    {
        'title': 'The Return of the King',
        'author_name': 'J.R.R. Tolkien',
        'price': 15.99,
        'publisher': 'Houghton Mifflin',
        'publish_date': '1955-10-20',
        'rating': 4.9,
        'availability': True,
        'picture': 'media/returnoftheking.jpg'
    },
]

def populate_database():
  """
  This function iterates through the books_data list and inserts each book into the database.
  """
  for book_data in books_data:
    # Get or create User object (if applicable to your model)
    user = CustomUser.objects.get(username="admin")  # Replace with appropriate logic to get user

    # Get or create Author object (if applicable to your model)
    author, created = Author.objects.get_or_create(name=book_data["author_name"])

    # Create a new Book object with data
    book = Book(
        category=book_data["category"],
        title=book_data["title"],
        publisher=book_data["publisher"],
        publish_date=book_data["publish_date"],
        rating=book_data["rating"],
        availability=book_data["availability"],
        price=book_data["price"],
        picture=book_data["picture"],
        user=user,  # Assign user ?
        author=author,  # Assign?
    )

    # Save the book object to the database
    book.save()

    print(f"Book '{book.title}' successfully added to database.")

# Run the populate_database function
if __name__ == "__main__":
  populate_database()
