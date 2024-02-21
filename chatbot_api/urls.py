from django.urls import path
from . import views

urlpatterns = [
    path('havens_ai/', views.havens_ai, name='havens_ai'),
]