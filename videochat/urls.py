from django.contrib import admin
from django.urls import path,include
from .views import video ,testing

urlpatterns = [
    # path('meeting/',videocall,name='videocall')
    path('video/',video,name='video'),
    path('testing/',testing,name='testing'),
]