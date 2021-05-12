from django import forms
from .models import Rating, Book


class RatingForm(forms.Form):
    books = Book.objects.all().order_by('id')[:20]
    liked = forms.BooleanField(required=False)
    disliked = forms.BooleanField(required=False)
