from django.db import models
from django.db.models.fields import *
from member.models import User

# Create your models here.

#채팅
class Chat(models.Model):
    chat_id = models.AutoField(primary_key=True)
    chat_name = models.CharField(max_length=30, null=False)
    chat_password = models.CharField(max_length=30, null=True)
    chat_people = models.IntegerField(default=2, null=False)
    chat_flag = models.BooleanField(default=False, null=False)
    chat_info = models.CharField(max_length=255)
    reg_date = models.DateTimeField(auto_now_add=True, null=False)
    # fk
    #개설자
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, db_column='user_id')
 
    class Meta:
        db_table = 'chat'


#태그
class ChattingTag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=10, null=False, unique=True)

    class Meta:
        db_table = 'chatting_tag'


#채팅-태그 관계 테이블
class ChatTag(models.Model):
    #fk
    chat = models.ForeignKey(Chat, on_delete = models.CASCADE, null=False, db_column='chat_id')
    chattingTag = models.ForeignKey(ChattingTag, on_delete=models.CASCADE, null=False, db_column='tag_id')
 
    class Meta:
        db_table = 'chat_tag'


#채팅-회원 참여 관계 테이블
class ChatUser(models.Model):
    #fk
    chat = models.ForeignKey(Chat, on_delete = models.CASCADE, null=False, db_column='chat_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, db_column='user_id')
 
    class Meta:
        db_table = 'chat_user'