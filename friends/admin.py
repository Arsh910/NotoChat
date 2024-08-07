from django.contrib import admin
from .models import notifyFriend,friendList
# Register your models here.
admin.site.register(friendList)
admin.site.register(notifyFriend)