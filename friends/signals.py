from django.shortcuts import redirect
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, friendList


@receiver(post_save, sender=Profile)
def create_friend_list(sender, instance, created, **kwargs):
    if created:
        friendList.objects.create(user=instance)
