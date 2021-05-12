from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404
from .models import Book, Rating
from django.http import HttpResponseRedirect


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def recommend(request):
    bookList = Book.objects.all()
    # zde nebude Book.objects.all(), ale knihy doporucene algoritmem kolaborativniho filtrovani
    context = {'recommended_books': bookList}
    return render(request, 'recommend.html', context)


def prefer(request):
    books_part_one = Book.objects.all().order_by('id')[:10]
    books_part_two = Book.objects.all().order_by('-id')[:10]
    context = {'books_part_one': books_part_one, 'books_part_two': books_part_two}
    return render(request, 'prefer.html', context)


def likeView(request):
    book_liked = get_object_or_404(Book, id=request.POST.get('book_like_id'))
    if Rating.objects.filter(book=book_liked, user=request.user).exists():
        rating = Rating.objects.filter(book=book_liked, user=request.user).first()
        rating.liked = True
        rating.save()
    else:
        Rating.objects.create(liked=True, book=book_liked, user=request.user)
    return HttpResponseRedirect(reverse('prefer'))


def dislikeView(request):
    book_disliked = get_object_or_404(Book, id=request.POST.get('book_dislike_id'))
    if Rating.objects.filter(book=book_disliked, user=request.user).exists():
        rating = Rating.objects.filter(book=book_disliked, user=request.user).first()
        rating.liked = False
        rating.save()
    else:
        Rating.objects.create(liked=False, book=book_disliked, user=request.user)

    return HttpResponseRedirect(reverse('prefer'))
