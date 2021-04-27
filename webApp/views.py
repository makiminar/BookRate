from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import Book
from .forms import RatingForm


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
    form = RatingForm(request.POST or None)
    if form.is_valid():
        result = form.save(commit=False)
        result.user = request.user
        result.save()
    context['form'] = form
    return render(request, 'prefer.html', context)
