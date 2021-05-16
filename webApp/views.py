from math import sqrt

from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404
from .models import Book, Rating, Recommendation
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class TmpUser:
    user = get_user_model()
    userMean = 0.0


def recommend(request):
    bookList = Book.objects.all()
    # zde nebude Book.objects.all(), ale knihy doporucene algoritmem kolaborativniho filtrovani
    context = {'recommended_books': bookList}
    return render(request, 'recommend.html', context)


def prefer(request):
    books_part_one = Book.objects.all().order_by('id')[:10]
    books_part_two = Book.objects.all().filter(pk__in=[11,12,13,14,15,16,17,18,19,20]).order_by('id')
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


def recommendView(request):
    activeUser = request.user
    User = get_user_model()
    similarityDict = {}
    recommendDict = {}
    cnt, tmp = 0.0, 0.0
    for rating in Rating.objects.filter(user=activeUser):
        if rating.liked:
            tmp += 1
        else:
            tmp -= 1
        cnt += 1
    activeUserMean = tmp/cnt

    # Calculate similarity of all other users
    for user in User.Objects.where(id != activeUser.id).all():
        TmpUser.user = user
        userMean, cnt, Ryi, Rxi, sum1, sum2, sum3 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        for rating in Rating.objects.filter(user=TmpUser.user):
            if rating.liked:
                tmp += 1.0
            else:
                tmp -= 1.0
            cnt += 1.0
        TmpUser.userMean = tmp / cnt
        for book in Book.objects.all():
            if Rating.objects.filter(book=book, user=TmpUser.user).exists():
                rating = Rating.objects.filter(book=book, user=TmpUser.user).first()
                if rating.liked:
                    Ryi = 1.0
                else:
                    Ryi = -1.0
            else:
                Ryi = 0.0
            if Rating.objects.filter(book=book, user=activeUser).exists():
                rating = Rating.objects.filter(book=book, user=activeUser).first()
                if rating.liked:
                    Rxi = 1.0
                else:
                    Rxi = -1.0
            else:
                Rxi = 0.0

            sum1 += (Rxi - activeUserMean)*(Ryi - userMean)
            sum2 += (Rxi - activeUserMean)**2
            sum3 += (Ryi - userMean)**2
        similarityScore = sum1 / (sqrt(sum2) * sqrt(sum3))
        similarityDict[TmpUser] = similarityScore

    sumOfSims = 0.0

    for key in similarityDict:
        sumOfSims += abs(similarityDict.get(key))
    normalizingFactor = 1.0/sumOfSims

    for book in Book.objects.filter(pk__in=[21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]):
        sum4 = 0.0
        for key, item in similarityDict.items():
            if Rating.objects.filter(book=book, user=key.user).exists():
                rating = Rating.objects.filter(book=book, user=key.user).first()
                if rating.liked:
                    Ryi = 1.0
                else:
                    Ryi = -1.0
            else:
                Ryi = 0
            sum4 += item * (Ryi - key.userMean)
        recommendDict[book] = activeUserMean + (normalizingFactor*sum4)

    sortedDict = sorted(recommendDict.items(), key=lambda it: it[1], reverse=True)
    if Recommendation.objects.filter(user=activeUser).exists():
        rec = Recommendation.objects.filter(user=activeUser).first()
        rec.firstId = sortedDict[0].id
        rec.secondId = sortedDict[2].id
        rec.thirdId = sortedDict[4].id
        rec.fourthId = sortedDict[6].id
        rec.fifthId = sortedDict[8].id
    else:
        Recommendation.objects.create(user=activeUser,
                                      firstId=sortedDict[0].id,
                                      secondId=sortedDict[2].id,
                                      thirdId=sortedDict[4].id,
                                      fourthId=sortedDict[6].id,
                                      fifthId=sortedDict[8].id)


