from django import forms
from .models import BookReview

class BookReviewForm(forms.ModelForm):
    review=forms.CharField(widget=forms.Textarea(attrs={'user': ' write your review here'}))
    class Meta:
        model = BookReview
        fields = ['review', 'rating']