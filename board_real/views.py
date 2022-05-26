from distutils.command.upload import upload
from unicodedata import category
from unicodedata import name
from django.http import HttpResponseNotFound, HttpResponseRedirect, Http404, response
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from .forms import * 
from .models import *
from django.db import transaction
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .models import Board,User
def index(request):

    replys = Reply.objects.filter(reply_deleted='N')
    replycnt = replys.count()
    
    #페이징
    page = request.GET.get('page', '1')  # 페이지
    # 조회
    question_list = Board.objects.filter(board_deleted='N').order_by('-board_reg_date')
    # 페이징처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj,'replycnt' : replycnt}
    return render(request, 'board_real/list.html', context)


# @login_required
@transaction.atomic
def post(request):
    try:
        if request.method == "POST":
            board_title = request.POST['board_title']
            board_content = request.POST['board_content']
            category_name = request.POST['category_name']
            category = Category.objects.get(category_name=category_name)
            user_id=request.session.get('user_id')
            user = User.objects.get(pk=user_id)
            board = Board(
                board_title=board_title, 
                board_content=board_content, board_reg_date = timezone.now(),
                category=category, user=user )
            board.save()
            # 파일업로드 
            myfile=request.FILES.get('myfile')
            if myfile:
                fs = FileSystemStorage() # 실제 파일이 저장되고
                file = File(file_name='uploads/'+myfile.name, board=board) # db에 저장
                file.save()
                filename = fs.save('uploads/'+myfile.name, myfile)
                uploaded_file_url = fs.url(filename)
            return redirect('board_real:index')
        else:
            return render(request, 'board_real/post.html')
    except:
        return HttpResponseNotFound(content='404 NOT FOUND')


import os
def boardview(request):
    #form 처리
    if request.method == 'POST':
        if 'report_flag' in request.POST:
            form = ReportLikeForm(request.POST)
            cboard = Board.objects.get(board_id = form.data['board_id'])
            cuser = User.objects.get(user_id = form.data['user_id'])
            if form.data['reply_id'] != '-1':
                creply = creply = Reply.objects.get(reply_id = form.data['reply_id'])
            if form.data['report_flag'] == 'l':
                if form.data['reply_id'] != '-1':
                    ReplyLikeReport.objects.create(reply = creply, user=cuser, like_YN = 'Y')
                    creply.reply_like_cnt += 1
                    creply.save()
                    return redirect('/board_real/board_view?id='+form.data['board_id'])
                cboard.user_like.add(cuser)
                cboard.board_like_cnt += 1
                cboard.save()
                return redirect('/board_real/board_view?id='+form.data['board_id'])
            if form.data['report_flag'] == 'r':
                if form.data['reply_id'] != '-1':
                    ReplyLikeReport.objects.create(reply = creply, user=cuser, like_YN = 'N')
                    creply.reply_dis_cnt += 1
                    creply.save()
                    return redirect('/board_real/board_view?id='+form.data['board_id'])
                cboard.user_report.add(cuser)
                cboard.board_dis_cnt += 1
                cboard.save()
                return redirect('/board_real/board_view?id='+form.data['board_id'])
            if form.data['report_flag'] == 'b':
                if form.data['reply_id'] != '-1':
                    replymark, rflag = ReplyBookmark.objects.get_or_create(reply = creply, user = cuser)
                    if not rflag:
                        replymark.use_YN = 'Y'
                        replymark.save()
                    return redirect('/board_real/board_view?id='+form.data['board_id'])
                boardmark,bflag = BoardBookmark.objects.get_or_create(board = cboard, user = cuser)
                if not bflag:
                    boardmark.use_YN = 'Y'
                    boardmark.save()
                return redirect('/board_real/board_view?id='+form.data['board_id'])
            if form.data['report_flag'] == 'c':
                if form.data['reply_id'] != '-1':
                    Rreply = ReplyBookmark.objects.get(reply = creply)
                    Rreply.use_YN = 'N'
                    Rreply.save()
                    return redirect('/board_real/board_view?id='+form.data['board_id'])
                Bboard = BoardBookmark.objects.get(board = cboard, user = cuser)
                Bboard.use_YN = 'N'
                Bboard.save()
                return redirect('/board_real/board_view?id='+form.data['board_id'])
            return HttpResponse('reportflag detected')
        if 'delete_YN' in request.POST:
            form = DeleteBoardForm(request.POST)
            b_id = form.data['id']
            if form.data['delete_YN'] == 'Y':
                b = Board.objects.get(board_id = b_id)
                b.board_deleted = 'Y'
                b.save()
                return redirect('/board_real/list')
            else:
                b = Reply.objects.get(reply_id = b_id)
                b.reply_deleted='Y'
                b.save()
                return redirect('/board_real/board_view?id='+form.data['board_id'])
        else:
            form = ReplyForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data['reply_content']
                uid = form.data['user_id']
                bid = form.data['board_id']
                Reply.objects.create(reply_content=content, reply_deleted = 'N', user_id = uid, board_id = bid)
                return redirect('/board_real/board_view?id='+form.data['board_id'])
            else:
                return redirect('/board_real/board_view?id='+form.data['board_id'])
    
    reqId = request.GET.get('id')
    
    try:
        board= Board.objects.get(board_id=reqId)
    except:
        #return HttpResponse('<h1>요청하신 페이지를 찾을 수 없습니다</h2>')
        return HttpResponseNotFound(content='404 NOT FOUND')
    if board.board_deleted == 'Y':
        return HttpResponseNotFound(content='404 NOT FOUND')
    replys = Reply.objects.filter(board_id = reqId, reply_deleted='N')
    category = board.category.category_name
    user = User.objects.get(user_id = board.user.user_id)
    replycnt = replys.count
    formlike = ReportLikeForm()
    formdelete = DeleteBoardForm()
    formreply = ReplyForm()

    try:
        boardBookmarked = BoardBookmark.objects.filter(board_id = board.board_id, use_YN = 'Y')
    except:
        boardBookmarked = None
    try:
        replyBookmarked = ReplyBookmark.objects.filter( reply__in = replys, use_YN = 'Y')
    except:
        replyBookmarked = None
    try:
        replyLike = ReplyLikeReport.objects.filter(reply__in = replys, like_YN = 'Y')
    except:
        replyLike = None
    try:
        replyReport = ReplyLikeReport.objects.filter(reply__in = replys, like_YN = 'N')
    except:
        replyReport = None
    board.view_cnt += 1
    board.save()
    return render(request, 'board_real/board_view.html',
    {'board':board, 'replys':replys,
    'category':category, 'user':user, 'replycnt':replycnt,
    'formlike':formlike, 'formdelete':formdelete, 'boardBookmarked':boardBookmarked,
    'formreply':formreply, 'replyBookmarked':replyBookmarked, 'replyLike':replyLike, 'replyReport':replyReport
     })
    

def detail(request, post_id):
    try:
        board = Board.objects.get(pk=post_id)
    except Board.DoesNotExist:
        raise Http404("Does not exist!")
    return render(request, 'board_real/detail.html', {'board': board})



def FreeListView(request):
    # free_list=Board.objects.filter(category_id=2).order_by('-board_reg_date')
    # context = {'free_list': free_list}
    # return render(request, 'board_real/free_list.html', context)

    page = request.GET.get('page', '1')
    free_list = Board.objects.filter(category_id=2).order_by('-board_reg_date')
    paginator = Paginator(free_list, 10)
    page_obj = paginator.get_page(page)
    context = {'free_list': page_obj}
    return render(request, 'board_real/free_list.html', context)

def QnaListView(request):
    # qna_list=Board.objects.filter(category_id=3).order_by('-board_reg_date')
    # context2 = {'qna_list': qna_list}
    # return render(request, 'board_real/qna_list.html', context2)

    page = request.GET.get('page', '1')
    qna_list = Board.objects.filter(category_id=3).order_by('-board_reg_date')
    paginator = Paginator(qna_list, 10)
    page_obj = paginator.get_page(page)
    context = {'qna_list': page_obj}
    return render(request, 'board_real/qna_list.html', context)

def JobListView(request):
    # job_list=Board.objects.filter(category_id=4).order_by('-board_reg_date')
    # context3 = {'job_list': job_list}
    # return render(request, 'board_real/job_list.html', context3)

    page = request.GET.get('page', '1')
    job_list = Board.objects.filter(category_id=4).order_by('-board_reg_date')
    paginator = Paginator(job_list, 10)
    page_obj = paginator.get_page(page)
    context = {'job_list': page_obj}
    return render(request, 'board_real/job_list.html', context)

def download(request):
    id = request.GET.get('id')
    board = Board.objects.get(pk=id)

    file=File.objects.get(board=board)
    if file!=None: #파일이 존재할떄
        filepath = str(settings.BASE_DIR) + ('/media/%s'%(file.file_name))
        filename = os.path.basename(filepath)
        filetype=filename.split('.')[-1]
        with open(filepath, 'rb') as f:
            FileDownload = HttpResponse(f, content_type='application/octet-stream')
            FileDownload['Content-Disposition'] = 'attachment; filename=%s' % (filename)

        return FileDownload
    
    else:
      return HttpResponse('파일 접근 불가')

    
from django.db.models import Q
def search(request):
    content_list = Board.objects.all()
    search = request.GET.get('search','')
    if search:
        search_list = content_list.filter(
            Q(board_title__icontains = search) | #제목
            Q(board_content__icontains = search)  #내용
    )
    else:
        return redirect('/board_real/list')

    paginator = Paginator(search_list,5)
    page = request.GET.get('page','')
    posts = paginator.get_page(page)
    board = Board.objects.all()

    return render(request, 'board_real/search.html',{'posts':posts,'Board':board,'search':search})
    
