from django.shortcuts import render
from .models import GroupMessage ,ChatGroup
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,redirect
from django.http import Http404
from django.contrib import messages
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import HttpResponse


from User_profile.models import Profile

# Create your views here.
@login_required
def chat(requests,chatroom):
    chat_group = get_object_or_404(ChatGroup,group_name=chatroom)
    mesg = chat_group.chat_messages.all()[:20] #to the get the messages related to group with related name
    
    author = requests.user
    chatrooms = ChatGroup.objects.all()
    k=[]
    d=[]
    for chat in chatrooms:
        
        if author in chat.memebers.all():
            
            if chat.groupchat_name:
                d.append(chat)
            if  chat.is_private==True:
                for c in chat.memebers.all():
                    if(c!=author): 
                        k.append({'c':c,'chat':chat})

    other_user = None
    if chat_group.is_private:
        if requests.user not in chat_group.memebers.all():
            raise Http404()
        
        for memeber in chat_group.memebers.all():
            if memeber != requests.user:
                other_user = memeber
                break
    
    if chat_group.groupchat_name:
        if requests.user not in chat_group.memebers.all():
            if requests.user.emailaddress_set.filter(verified = True).exists():
                chat_group.memebers.add(requests.user)
            else:
                messages.warning(requests,'You need to verify you email')
                return redirect('/')
    
    # if requests.htmx:
    #     data = requests.POST 
    #     if data:
    #         message = data.get('message')
    #         group  =  chat_group
    #         author  = requests.user

    #         obj = GroupMessage.objects.create(
    #             group = group,
    #             author = author,
    #             body = message,
    #         )
    #         obj.save()

    #         context = {
    #             'message':message,
    #             'author':author
    #         }

    #         return render(requests,'chat_message_p.html',context)
    return render(requests,'chatpagenew.html',{'mesg':mesg,'count':chat_group.user_online.count()-1,'other_user':other_user,'chatroom':chatroom ,'groupname':chat_group.groupchat_name ,'room':k,'groupchats':d}) 

@login_required
def get_or_creteroom(request,username):
    other_user = Profile.objects.get(username=username)
    my_chatroom = request.user.chat_groups.filter(is_private=True)
    print(my_chatroom)
    if my_chatroom.exists():
        for chatroom in my_chatroom:
            if other_user in chatroom.memebers.all():
                chatroom = chatroom 
                break
            else:
                chatroom.memebers.add(other_user,request.user)
    else:
        chatroom = ChatGroup.objects.create(
                is_private = True
            )
        chatroom.memebers.add(other_user,request.user)
        chatroom.save()

    return redirect('chatroom',chatroom.group_name)

def create_group(requests):
    
    if requests.method == 'POST':
        data = requests.POST
        if data:
          name = data['name']
          obj = ChatGroup.objects.create(
              groupchat_name = name,
              group_admin = requests.user,  
          )
          obj.memebers.add(requests.user)
          obj.save()
        return redirect('chatroom',obj.group_name)
    
    return render(requests,'create.html')


def chatroom_leave(requests,chatroom):
    chat_group = get_object_or_404(ChatGroup,group_name=chatroom)
    if requests.user not in chat_group.memebers.all():
        raise Http404()    
        
    if requests.method == 'POST':
        if requests.user in chat_group.memebers.all():
            chat_group.memebers.remove(requests.user)

    messages.success(requests,'you left the chat')
    return redirect('home') 

def chat_file(request,chatroom):
    chat_group=get_object_or_404(ChatGroup,group_name = chatroom)

    chatroom_name_sanitized = chat_group.group_name.replace(' ', '_')

    if request.method == 'POST':
        print(request.FILES.get("file"))
        message = GroupMessage.objects.create(
            file = request.FILES.get("file"),
            author = request.user,
            group = chat_group
        )   
        message.save()

        channel_layer = get_channel_layer()

        event = {
            'type':'message_handler',
            'message_id':message.id
        }

        async_to_sync(channel_layer.group_send)(
            chatroom_name_sanitized,event
        )
    return HttpResponse()


def chathome(requests,username):
    if requests.user.username == username:

        author = requests.user
        chatrooms = ChatGroup.objects.all()
        k=[]
        d=[]
        for chat in chatrooms:
            print(f"members are {chat.memebers.all()}")
            if author in chat.memebers.all():
                print("hello")
                if chat.groupchat_name:
                    d.append(chat)
                if  chat.is_private==True:
                    for c in chat.memebers.all():
                        if(c!=author): 
                            k.append({'c':c,'chat':chat})


        return render(requests,'hometext.html',{'name' : username,'room':k,'groupchats':d})
    else:
        return messages(Warning,'sorry you are not allowed')