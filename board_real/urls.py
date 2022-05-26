from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'board_real'
urlpatterns = [
        path('board_view/', views.boardview, name='board_view'),
        path('list/', views.index, name='index'),
        path('post/', views.post, name='post'),
        path('post/<int:post_id>/', views.detail, name='detail'),

        path('free/', views.FreeListView, name='free_list'), #자유
        path('qna/', views.QnaListView, name='qna_list'),  #수업 Q&A
        path('job/', views.JobListView, name='job_list'),  #취업 준비
        path('download/', views.download, name='download'),
        path('search/',views.search, name="search"), #글 검색
] 
#파일 추가를위한거 
# + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
#     import debug_toolbar
    urlpatterns += [
        # path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
