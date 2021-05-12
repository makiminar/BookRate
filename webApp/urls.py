from django.urls import path
from .views import SignUpView, recommend, prefer, likeView, dislikeView

urlpatterns = [
  path('signup/', SignUpView.as_view(), name='signup'),
  path('prefer/', prefer, name='prefer'),
  path('recommend/', recommend, name='recommend'),
  path('like/', likeView, name='like_post'),
  path('dislike/', dislikeView, name='dislike_post'),
]
