# Our Book Shop
## Overview
This is an online shop project built with Django, which allows users to browse, purchase, and manage books. The online shop project includes features such as viewing book details, adding books to the shopping cart, managing the shopping cart, wishlists, and placing orders. There is also a second Django project included with two APIs for genres and contact. These APIs are used to display the genre and contact information in our online shop project.
## Features
    - Users can sign up, log in, log out and edit their profile information.
    - Admins can add new books to the shop.
    - Book Listing: Users can browse through a list of available books.
    - Book Detail: Users can view detailed information about a specific book.
    - Add to Wishlist: Users can add books to their wishlist.
    - Remove from Wishlist: Users can remove books from their wishlist.
    - View Wishlist: Users can view the contents of their wishlist.
    - Add to Cart: Users can add books to their shopping cart from book list or from wishlist.
    - Remove from Cart: Users can remove books from their shopping cart.
    - View Cart: Users can view the contents of their shopping cart, including total prices.
    - Order Placement: Users can place orders for the books in their shopping cart.
    - Payment Methods: Users can choose to pay via PayPal or via bank transfer.
    - Order Confirmation: Users receive confirmation after placing an order.
    - Update Book Inventory upon Order Placement/Database Maintenance: When users place an order for books in their shopping cart, the system automatically reduces the available quantity of each ordered book from the database.
**This project is part of the Python Backend Programming course from DCI Institute:**
[DCI Python Course](https://digitalcareerinstitute.org/courses/python-backend-programming/)
## Development Setup
Before you begin, ensure you have met the following requirements:
- **Python:** This project is developed using Python 3.10.12. Make sure you have Python installed on your system. You can download it from [python.org](https://www.python.org/).
- **Integrated Development Environment (IDE):**
This entire application is built using Visual Studio Code.
- **Virtual Environment (Optional, but recommended):** It's a good practice to use a virtual environment for Python projects. You can create one using the `venv` module or `virtualenv`.
Open a terminal and navigate to the project directory. Use the command:
```
On Windows    : python -m venv venv
On macOS/Linux: python3 -m venv venv
```
- **Activate the virtual environment:**
```
On Windows    : .\venv\Scripts\activate
On macOS/Linux: source venv/bin/activate
```
- **Install Dependencies:**
```
On Windows    : pip install -r requirements.txt
On macOS/Linux: pip3 install -r requirements.txt
```
- **Navigate to the outer Django project directory in your terminal and run the project from here.**
## Project Execution
- **Database Settings (online_shop project):**
- Edit online_shop/online_shop/settings.py.
- Choose between SQLite3 (default) or Postgres.
- For Postgres, update DATABASES with your credentials.
```
DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.postgresql',
         'NAME': 'book_shop_db', # Provide your database name
         'USER': 'xxxxxx', # Provide your database username
         'PASSWORD': 'xxxxxx', # Provide your database password
         'HOST': 'localhost', # Provide your database host
         'PORT': '5432', # Provide your database port
     }
 }
```
- **Database Migration (online_shop project):**
```
On Windows    : python manage.py makemigrations
                python manage.py migrate
On macOS/Linux: python3 manage.py makemigrations
                python3 manage.py migrate
```
- **Run Development Server (online_shop project):**
```
On Windows    : python manage.py runserver
On macOS/Linux: python3 manage.py runserver
```
- **Run Tests:**
The code for the tests can be seen in the file fee_calculator/tests.
To run the tests, use the following command in your terminal:
```
On Windows    : python manage.py test
On macOS/Linux: python3 manage.py test
```
## API Project Setup:
- Navigate to the api_project directory.
- Activate your virtual environment (if used) like explained above.
- Follow the same steps as above to install dependencies.
- Follow the same database setup and migration steps as the online_shop project.
- Run development server: python manage.py runserver (use port 5000: python manage.py runserver 5000)
## API Integration
The project integrates with two APIs (inlcuded in the folder api_project) to fetch contact information and book genres. It uses the following endpoints:
    http://127.0.0.1:5000/api/contacts/: Retrieves contact information.
    http://127.0.0.1:5000/api/contacts/<contact_id>/: Retrieves details of a specific contact.
    http://127.0.0.1:5000/api/genres/: Retrieves book genres.
    http://127.0.0.1:5000/api/genres/<genre_id>/: Retrieves details of a specific genre.
## Usage
    Access the online shop in your web browser at http://localhost:8000.
    Browse through available books, add them to your cart or wishlist, and proceed with the checkout process.
## Contributors
    Natalie Dutz    https://github.com/nataliedutz
    Kamal Chabouk   https://github.com/kamalchabouk/
    René Wuttig     https://github.com/Rene-Wuttig
## License
This project is licensed under the [MIT](https://github.com/ADD PATH TO LICENSE.txt) License.
Digital Career InstituteDigital Career Institute
Become a Python programmer expert – with certificate
llll➤ Start a Python Backend course remotely online.:heavy_check_mark: 600+ company partners.:heavy_check_mark:3000+ participants & alumni.:heavy_check_mark:Join today!
Est. reading time
1 minute
Python.orgPython.org
Welcome to Python.org
The official home of the Python Programming Language
