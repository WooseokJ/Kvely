from django.urls import path
from . import views

app_name = 'member'
urlpatterns = [
        path('signup/', views.signup, name='signup'),
        path('login/', views.login, name='login'),
        path('logout/', views.logout, name='logout'),
        path('mypage/', views.mypage, name='mypage'),
        path('edit/', views.editUser, name='edit'),
        path('chat/', views.manageChat, name='chat'),
        path('delete/', views.deleteUser, name='delete'),
        path('randomnick/', views.randomNick, name='random'),
        path('more/board/', views.boardmore, name='board'),
        path('more/bbookmark/', views.bbookmarkmore, name='bbookmark'),
        path('more/reply/', views.replymore, name='reply'),
        path('more/rbookmark/', views.rbookmarkmore, name='rbookmark'),
]
