from django.contrib import admin
from .models import Book, User, Rating
# Register your models here.

admin.site.register(Book)
admin.site.register(User)
admin.site.register(Rating)
