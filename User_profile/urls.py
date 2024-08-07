from django.contrib import admin
from django.urls import path,include
from .views import hello ,profile,search

urlpatterns = [
    path('',hello,name='home'),
    path('profile/<str:username>/',profile,name='profile'),
    path('search/',search,name='profile'),
]