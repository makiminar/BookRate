from django.contrib import admin
from .models import Book, Rating
# Register your models here.

admin.site.register(Book)
admin.site.register(Rating)

"""class UserProfile(models.Model):
    user = models.OneToOneField(User,  on_delete=models.CASCADE)


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User) """