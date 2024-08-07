from django.db import models
import shortuuid
from User_profile.models import Profile
# Create your models here.

class Video_room(models.Model):
    name = models.CharField(max_length=128,unique=True,default=shortuuid.uuid)
    memebers = models.ManyToManyField(Profile , related_name='video_members',blank=True )
    v_author = models.ForeignKey(Profile , related_name='v_author',blank=True , on_delete=models.CASCADE)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Video_text_chat(models.Model):
    name = models.CharField(max_length=20,default='Video_text_room')
    memebers = models.ManyToManyField(Profile , related_name='video_text_members',blank=True )
    is_random = models.BooleanField(default=True)

    def __str__(self):
        return self.name