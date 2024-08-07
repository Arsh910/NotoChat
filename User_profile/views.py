from django.shortcuts import render ,get_object_or_404
from .models import Profile
from chat.models import ChatGroup
from django.contrib import messages
from django.http import JsonResponse
from friends.models import notifyFriend , friendList
from allauth.account.views import LoginView


# Create your views here.
def hello(request):
    author = request.user
    chatrooms = ChatGroup.objects.all()
    context={}
    k=[]
    d=[]
    for chat in chatrooms:
        if author in chat.memebers.all():
            if chat.groupchat_name:
                d.append(chat)
            for c in chat.memebers.all():
                if(c!=author): 
                    k.append(c)
    context={'room':k,'groupchats':d}
    # messages.info(request,'Checking')
    return render(request,'home.html',context)

def profile(request,username):
    author = Profile.objects.get(username=username)
    l  = friendList.objects.get(user = request.user)
    list = l.friend_list.all()
    count = list.count()
    return render(request,'profile.html',{'auth':author,'list':list,'count':count})

def search(requests):
    t=list()
    search = requests.GET.get('search')        
    if search:
            result = Profile.objects.filter(Q(username__contains = str(search)) | Q(username__startswith = str(search)) | Q(username__endswith = str(search)))
            for res in result:
                if res.id:
                    t.append(dict(
                            {
                            'username':res.username,
                            'id':res.id,
                            }
                            ))
                else:
                    t.append(dict(
                            {
                            'username':res.username,
                            'profile_pic':res.id,
                            }
                            ))

            return JsonResponse({
            'payload' : t
            })
    top = Profile.objects.all()
    return render(requests,'search_user.html',{'top':top})