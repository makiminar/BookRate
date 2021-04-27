from django.urls import path
from .views import SignUpView, recommend, prefer

urlpatterns = [
  path('signup/', SignUpView.as_view(), name='signup'),
  path('prefer/', prefer, name='prefer'),
  path('recommend/', recommend, name='recommend'),
]
