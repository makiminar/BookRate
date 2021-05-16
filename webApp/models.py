from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=40)

    def __str__(self):
        return self.title


class Rating(models.Model):
    liked = models.BooleanField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True)


class Recommendation(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True,)
    firstId = models.CharField(max_length=5, null=True)
    secondId = models.CharField(max_length=5, null=True)
    thirdId = models.CharField(max_length=5, null=True)
    fourthId = models.CharField(max_length=5, null=True)
    fifthId = models.CharField(max_length=5, null=True)

