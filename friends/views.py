from django.shortcuts import render,get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages , redirects
from .models import notifyFriend , friendList
from User_profile.models import Profile
from django.http import JsonResponse
import json

# Create your views here.

@login_required
def send(requests,username):
    if requests.method == 'POST':
        to_whom = Profile.objects.get(username=username)
        
        k = notifyFriend.objects.filter(from_who = requests.user,to_who = to_whom,)

        if k:
            return JsonResponse('requests already sent',safe=False)
        else:      
            obj = notifyFriend.objects.create(
                from_who = requests.user,
                to_who = to_whom,
            )
            obj.save()
            return JsonResponse('requests sent',safe=False)
        
@login_required
def cancel(requests,username):
    if requests.method == 'POST':
        to_whom = Profile.objects.get(username=username)
        k = notifyFriend.objects.filter(from_who = requests.user,to_who = to_whom,)
        if k:
            k.delete()
            return JsonResponse('request cancelled',safe=False)
        else:
            return JsonResponse('You did not sent a request',safe=False)

@login_required
def accept(requests,username):
    if requests.method == 'POST':
        kf = Profile.objects.get(username = username)
        ks = notifyFriend.objects.filter(to_who = requests.user,from_who=kf ,is_accepted = False,is_decline = False)
        ku = friendList.objects.get(user=kf)
        k = notifyFriend.objects.filter(to_who = requests.user ,is_accepted = False,is_decline = False)
        if  ks:
            ks.update(
                is_accepted = True
            )
            ku.friend_list.add(requests.user)
            return JsonResponse('accepted',safe=False)
        
@login_required
def decline(requests,username):
    if requests.method == 'POST':
        kf = Profile.objects.get(username = username)
        ks = notifyFriend.objects.filter(to_who = requests.user,from_who=kf ,is_accepted = False,is_decline = False)
        ku = friendList.objects.get(user=kf)
        k = notifyFriend.objects.filter(to_who = requests.user ,is_accepted = False,is_decline = False)
        if  ks:
            ks.update(
                is_accepted = False,
                is_decline = True
            )
            ku.friend_list.add(requests.user)
            return JsonResponse('declined',safe=False)
        
@login_required
def start_not(requests):
        
        k =notifyFriend.objects.filter(to_who = requests.user ,is_accepted = False,is_decline = False)
        all=[]
        for el in k:
            all.append({
                    'username' : el.from_who.username,
                    'photo' : el.from_who.prof_image.url
            })

        return render(requests,'notifications.html',{'data':all,'length':len(all)})           
