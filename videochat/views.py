from django.shortcuts import render ,get_object_or_404 ,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Video_room
from User_profile.models import Profile
# Create your views here.

# @login_required

# def videocall(requests):
#     return render(requests,'WEB_UIKITS.html',{'name':requests.user})

@login_required

def video(requests):
    if requests.method == 'POST':
        data = requests.POST
        videoroom = data.get('name')
        room = Video_room.objects.filter(name = videoroom)
        num = Profile.objects.all().count()

        if room:
            k = Video_room.objects.get(name = videoroom)
            created = 'join'
            k.memebers.add(requests.user)
            return render(requests,'video.html',{'created':created,'name':videoroom , 'auname':k.v_author ,'num':num})
        
        else:
            created = 'created'
            obj = Video_room.objects.create(
                name = videoroom,
                v_author = requests.user
            )
            obj.memebers.add(requests.user)
            messages.success(requests,'Created a chat room for you')
            return render(requests,'video.html',{'created':created,'name':videoroom,'auname':requests.user,'num':num})
        
    return redirect('/')


def testing(requests):
        num = Profile.objects.all().count()
        return render(requests,'testing.html',{'num':num})
