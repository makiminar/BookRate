from django.db import models


# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=40)


class Rating(models.Model):
    rating_choices = (
        ('L', 'Liked'),
        ('D', 'Disliked')
    )
    rating = models.CharField(max_length=1, choices=rating_choices)
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True)
    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True)
