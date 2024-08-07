from django.contrib import admin
from django.urls import path
from .views import send,accept,start_not,cancel,decline

urlpatterns = [
    path('send_follow/<str:username>/',send,name="send_request"),
    path('cancel_follow/<str:username>/',cancel,name="send_request"),
    path('accept_follow/<str:username>/',accept,name="accept_request"),
    path('decline_follow/<str:username>/',decline,name="decline_request"),
    path('start_not/',start_not,name='start_not')
]