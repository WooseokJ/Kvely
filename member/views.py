from http.client import HTTPResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponse
from django.utils import timezone
from django.core.paginator import Paginator
from .models import User, Aivle, Noun, Adj
from board_real.models import Board, Reply, BoardBookmark, ReplyBookmark
import random

# Create your views here.

def login(request):
    if request.method == 'POST':
        user_email = request.POST.get('email')
        user_pw = request.POST.get('password')
        try:
            m = User.objects.get(user_email=user_email, user_pw=user_pw)
        except User.DoesNotExist as e:
            return render(request, 'member/login.html')
        else:
            request.session['user_id'] = m.user_id
            request.session['user_email'] = m.user_email
            request.session['user_nick'] = m.user_nick
            request.session['user_profile'] = m.user_profile
            print(request.session.get('user_id'), request.session.get('user_nick'))
            return redirect('/')      
    else:
       return render(request, 'member/login.html')


def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        code = request.POST.get('aivlecode')
        
        if password != password2:
            return redirect('member:signup')
        try:
            aivle = Aivle.objects.get(code = code)
            while True:
                adj = random.choice(Adj.objects.all())
                noun = random.choice(Noun.objects.all())
                nick = adj.first + ' ' + noun.second
                
                try: 
                    Aivle.objects.count(user_nick = nick)
                    continue;
                except:
                    break;
                
            m = User(
                user_email=email, 
                user_pw=password, 
                user_nick= nick, 
                user_track = '1',
                user_class = '1',
                aivle = aivle)
            m.save()
        except:
           return redirect('member:signup')
        return redirect('member:login')  
    
    else:
        return render(request, 'member/signup.html')

def logout(request):
    request.session.flush() # 전체 삭제
    return redirect('/')

def mypage(request):
    user_id = request.session.get('user_id', '0')
    
    if user_id == '0' :
        return redirect('member:login')
    else:
        user = User.objects.get(user_id = user_id)
        board_list = Board.objects.filter(user = user).filter(board_deleted='N').order_by('-board_id')[:5]
        reply = Reply.objects.filter(user=user).filter(reply_deleted='N').order_by('-reply_id')[:5]
        bbookmark = BoardBookmark.objects.filter(user=user).filter(use_YN = 'Y').order_by('-reg_date')[:5]
        rbookmark = ReplyBookmark.objects.filter(user=user).filter(use_YN='Y').order_by('-reg_date')[:5]
        return render(request, 'member/mypage.html', 
                      {'board_list':board_list,
                      'reply_list':reply,
                      'bbookmark_list':bbookmark,
                      'rbookmark_list':rbookmark})
    
def editUser(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id', '0')
        
        if user_id == '0' :
            return redirect('member:login')
        else:
            user = User.objects.get(user_id = user_id)
            
            password = request.POST.get('password')
            if password == "" :
                nick = request.POST.get('nick')
                user.user_nick = nick
                user.save()
                request.session['user_nick'] = nick
                return redirect('member:mypage')
            password2 = request.POST.get('password2')
            if password != password2:
                return redirect('member:edit')
            user.user_pw = password
            nick = request.POST.get('nick')
            user.user_nick = nick
            user.save()
            request.session.flush()
            return redirect('member:login')
    else:
        user_id = request.session.get('user_id')
        user = User.objects.get(user_id = user_id)
        
        return render(request, 'member/edit.html',{'user':user})

def manageChat(request):
    return HttpResponse('미구현')

def deleteUser(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        code = request.POST.get('aivlecode')
        user_id = request.session.get('user_id')
        
        try:
            user = User.objects.get(user_id = user_id)
            aivle = Aivle.objects.get(code = code)
        
            if user.user_pw == password and user.aivle == aivle :
                user.delete()
                request.session.flush() 
            
        except:
           return redirect('member:delete')
        return redirect('member:login')  
    
    else:
        return render(request, 'member/delete.html')

def randomNick(request):
    nick = ""
    while True:
        adj = random.choice(Adj.objects.all())
        noun = random.choice(Noun.objects.all())
        nick = adj.first + ' ' + noun.second
        
        try: 
            Aivle.objects.count(user_nick = nick)
            continue;
        except:
            break;
        
    return HttpResponse(nick)

def boardmore(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(user_id = user_id)
    replys = Board.objects.all()
    replycnt = replys.count
    #페이징
    page = request.GET.get('page', '1')  # 페이지
    # 조회
    question_list = Board.objects.filter(user=user).order_by('-board_id')
    # 페이징처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj,'replycnt' : replycnt}
    return render(request, 'member/boardmore.html', context)

def bbookmarkmore(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(user_id = user_id)
    replys = Board.objects.all()
    replycnt = replys.count
    question_list = []
    bbookmark = BoardBookmark.objects.filter(user=user).order_by('-board_id')
    #페이징
    page = request.GET.get('page', '1')  # 페이지
    # 조회
    question_list = Board.objects.prefetch_related('boardbookmark_set').filter(boardbookmark__user=user).filter(boardbookmark__use_YN='Y').order_by('-board_id')
    # 페이징처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj,'replycnt' : replycnt}
    return render(request, 'member/bbookmarkmore.html', context)

def replymore(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(user_id = user_id)
    question_list = []
    #페이징
    page = request.GET.get('page', '1')  # 페이지
    # 조회
    question_list = Reply.objects.filter(user=user).order_by('-reply_id')
    # 페이징처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj}
    return render(request, 'member/replymore.html', context)

def rbookmarkmore(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(user_id = user_id)
    question_list = []
    #페이징
    page = request.GET.get('page', '1')  # 페이지
    # 조회
    question_list = Reply.objects.prefetch_related('replybookmark_set').filter(replybookmark__user=user).filter(replybookmark__use_YN='Y').order_by('-reply_id')
    # 페이징처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj}
    return render(request, 'member/replymore.html', context)