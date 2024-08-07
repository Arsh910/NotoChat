from django.db import models
from User_profile.models import Profile
import shortuuid

# Create your models here.
class ChatGroup(models.Model):
    group_name = models.CharField(max_length=128 , unique = True , default=shortuuid.uuid)
    groupchat_name = models.CharField(max_length=128,null=True,blank=True)
    group_admin = models.ForeignKey(Profile,related_name='groupadmin',blank=True,null=True,on_delete=models.SET_NULL)
    user_online = models.ManyToManyField(Profile, related_name='online_in_groups',blank=True)
    memebers = models.ManyToManyField(Profile,related_name='chat_groups',blank=True)
    is_private = models.BooleanField(default=False)
    def __str__(self):
        return self.group_name

    
class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup , related_name='chat_messages',on_delete=models.CASCADE)
    author = models.ForeignKey(Profile , related_name='author',on_delete=models.CASCADE)
    body  = models.CharField(max_length=300,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='message_files',blank=True,null=True)
    
    def __str__(self):
        return self.author.username

    class Meta:
        ordering = ['-created']

    @property
    def is_image(self):
        if self.file.lower().endswith({'.jpg','.jped','.png','.svg','.webp'}):
            return True
        else:
            return False