from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    # path('chat_list/', views.chat_list, name='chatList'),    
    # path('mychat_list/', views.mychat_list, name='mychatList'),   
    # path('chat_form/', views.chat_form, name='chatForm'),
    # path('chat_del/', views.chat_del, name='chatDelete'),
    # path('chat_list/<int:chat_id>/', views.chat_in, name='chatIn'),   
    # path('chat_out/', views.chat_out, name='chatOut'),
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
    
]