from django.db import models
from User_profile.models import Profile

class friendList(models.Model):
    user = models.OneToOneField(Profile,related_name='of_friend',on_delete=models.CASCADE)
    friend_list = models.ManyToManyField(Profile,related_name='friend_list',blank=True)


class notifyFriend(models.Model):
    from_who = models.ForeignKey(Profile,related_name='from_who',on_delete=models.CASCADE)
    to_who   = models.ForeignKey(Profile,related_name='to_who',on_delete=models.CASCADE)
    send_on  = models.DateTimeField(auto_now=True)
    is_accepted = models.BooleanField(default=False)
    is_decline = models.BooleanField(default=False)


