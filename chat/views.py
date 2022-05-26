from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import User, ChattingTag, ChatTag, Chat, ChatUser
from django.db import transaction

# Create your views here.

#채팅방 리스트
def chat_list(request):
    chatList = Chat.objects.all()
    print(chatList)
    return render(request, 'chat/chat_list.html', {
        'data' : chatList
    })

#나의 채팅방 리스트
def mychat_list(request):
     #로그인 안 했을 때
    user_id = request.session.get('user_id')
    if user_id == None:
        return render(request, 'member/login.html', {})
    user = User.objects.get(user_id=user_id)
    chatList = ChatUser.objects.filter(user=user)
    print(chatList)
    return render(request, 'chat/mychat_list.html', {
        'data' : chatList
    })


#채팅방 생성
@transaction.atomic
def chat_form(request):
    user_id = request.session.get('user_id')
    #로그인 안 했을 때
    if user_id == None:
        return render(request, 'member/login.html', {})
    if request.method == 'POST':
        user = User.objects.get(user_id=user_id) #개설자
        chat_name = request.POST.get('name')
        chat_people = request.POST.get('people')
        chat_info = request.POST.get('info')
        tag_name = request.POST.get('tag')
        chat_flag = False
        if request.POST.get('flag') == 'True':
            chat_flag = True
        #DB insert
        chattingTag = ChattingTag()
        try:
            chattingTag = ChattingTag.objects.get(tag_name = tag_name)
        except ChattingTag.DoesNotExist:
            chattingTag = ChattingTag(tag_name = tag_name)
            chattingTag.save()
        chat = Chat(chat_name=chat_name, chat_people = chat_people, chat_info = chat_info, chat_flag = chat_flag, user=user)
        chat.save()
        chat_tag = ChatTag(chat = chat, chattingTag = chattingTag)
        chat_tag.save()
        #회원-채팅 참여에 개설자 넣기
        chatUser = ChatUser(chat=chat, user=user)
        chatUser.save()
        return redirect('chat:chatList')
    return render(request, 'chat/chat_form.html', {})

#채팅방 삭제
@transaction.atomic
def chat_del(request):
    chat_id=request.GET.get('chat_id')
    #삭제
    try:
        chat = Chat.objects.get(chat_id = chat_id)
        chat.delete()
        #참여하고있는 사람 다 삭제
        chatUser = ChatUser.objects.filter(chat_id = chat_id)
        chatUser.delete()
    except Chat.DoesNotExist:
        return redirect('chat:chatList')
    return JsonResponse("success", safe=False)


#채팅방 참여
@transaction.atomic
def chat_in(request, chat_id):
    user_id = request.session.get('user_id')
    #로그인 안 했을 때
    if user_id == None:
        return render(request, 'member/login.html', {})
    user = User.objects.get(user_id=user_id)
    chat = Chat()
    chatUser = ChatUser()
    try:
        chat = Chat.objects.get(chat_id = chat_id)
    except Chat.DoesNotExist:
         return redirect('chat:chatList')
    try:
        #이미 참여한 채팅방
        chatUser = ChatUser.objects.get(chat=chat, user=user)
    except ChatUser.DoesNotExist:
        chatUser =  ChatUser(chat=chat, user=user)
        chatUser.save()

    return render(request, 'chat/chat_room.html', {
        'data' : chat 
    })

#채팅방 나가기
@transaction.atomic
def chat_out(request):
    user_id = request.session.get('user_id')
    chat_id = request.GET.get('chat_id')
    #로그인 안 했을 때
    if user_id == None:
        return render(request, 'member/login.html', {})
    user = User.objects.get(user_id=user_id)
    chat = Chat()
    try:
        chat = Chat.objects.get(chat_id = chat_id)
    except Chat.DoesNotExist:
         return redirect('chat:mychatList')
    try:
        chatUser = ChatUser.objects.get(chat=chat, user=user)
        chatUser.delete()
    except ChatUser.DoesNotExist:
        return redirect('chat:mychatList')
    return JsonResponse("success", safe=False)


def index(request):
    return render(request, 'chat/index.html')

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })