from django.urls import path
from django.views.generic import TemplateView

from . import views
from .views import SignUpView

urlpatterns = [
  path('signup/', SignUpView.as_view(), name='signup'),
  path('prefer/', TemplateView.as_view(template_name='prefer.html'), name='prefer'),
  path('recommend/', views.recommend, name='recommend'),
]
