from django.urls import path
from .views import AddBookView, EditBookView,BookDeleteView

app_name = "forms" 

urlpatterns = [

    path('add_new_book/', AddBookView.as_view(), name= 'add_new_book' ),
    path('<int:pk>/edit/', EditBookView.as_view(), name= 'edit_book' ),
    path("<int:pk>/delete/", BookDeleteView.as_view(), name= 'delete_book'),
]