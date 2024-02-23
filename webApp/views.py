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
    if Recommendation.objects.filter(user=request.user).exists():
        rec = Recommendation.objects.filter(user=request.user).first()
        bookList = Book.objects.filter(pk__in=[rec.firstId, rec.secondId, rec.thirdId, rec.fourthId, rec.fifthId])
    else:
        bookList = []
    # zde nebude Book.objects.all(), ale knihy doporucene algoritmem kolaborativniho filtrovani
    context = {'recommended_books': bookList}
    return render(request, 'recommend.html', context)


def prefer(request):
    books_part_one = Book.objects.all().order_by('id')[:10]
    books_part_two = Book.objects.all().filter(pk__in=[11, 12, 13, 14, 15, 16, 17, 18, 19, 20]).order_by('id')
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
    activeUserMean = tmp / cnt

    # Calculate similarity of all other users
    for user in User.objects.all():
        if id != activeUser.id:
            TmpUser.user = user
            userMean, cnt, Ryi, Rxi, sum1, sum2, sum3 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
            for rating in Rating.objects.filter(user=TmpUser.user):
                if rating.liked:
                    tmp += 1.0
                else:
                    tmp -= 1.0
                cnt += 1.0
            if cnt != 0:
                TmpUser.userMean = tmp / cnt
            else:
                TmpUser.userMean = 0
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

                sum1 += (Rxi - activeUserMean) * (Ryi - userMean)
                sum2 += (Rxi - activeUserMean) ** 2
                sum3 += (Ryi - userMean) ** 2
            if sum2 != 0 and sum3 != 0:
                similarityScore = sum1 / (sqrt(sum2) * sqrt(sum3))
            else:
                similarityScore = 0
            similarityDict[TmpUser] = similarityScore

    sumOfSims = 0.0

    normalizingFactor = 0.0

    for key in similarityDict:
        sumOfSims += abs(similarityDict.get(key))
    if sumOfSims != 0:
        normalizingFactor = 1.0 / sumOfSims
    else:
        normalizingFactor = 0.0

    for book in Book.objects.filter(
            pk__in=[21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]):
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
        recommendDict[book] = activeUserMean + (normalizingFactor * sum4)

    sortedDict = sorted(recommendDict.items(), key=lambda it: it[1], reverse=True)
    arr = []
    for tup in sortedDict:
        arr.append(tup[0].id)

    if Recommendation.objects.filter(user=activeUser).exists():
        rec = Recommendation.objects.all().filter(user=activeUser).first()

        rec.firstId = arr[0]
        rec.secondId = arr[1]
        rec.thirdId = arr[2]
        rec.fourthId = arr[3]
        rec.fifthId = arr[4]
    else:
        Recommendation.objects.create(user=activeUser,
                                      firstId=arr[0],
                                      secondId=arr[1],
                                      thirdId=arr[2],
                                      fourthId=arr[3],
                                      fifthId=arr[4])

    return HttpResponseRedirect(reverse('recommend'))
