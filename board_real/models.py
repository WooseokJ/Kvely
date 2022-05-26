from django.db import models
from django.db.models.fields import *
from member.models import User

# Create your models here.
class Category(models.Model):
    category_id = AutoField(primary_key = True)
    category_name = CharField(max_length = 15 ,null = False)

    class Meta:
        db_table = 'category'
        managed=True


class Board(models.Model):
    board_id = AutoField(primary_key=True, db_column='board_id')
    board_title = CharField(max_length=50, null = False, db_column='board_title')
    board_content = TextField(max_length = None, null = False, db_column='board_content' )
    board_reg_date = DateTimeField(auto_now_add=True, null = False, db_column='board_reg_date')
    board_mod_date = DateTimeField(auto_now=True, null = True, db_column='board_mod_date')
    board_deleted = CharField(max_length=1, default = 'N', db_column='board_deleted')
    board_like_cnt = PositiveIntegerField(default = 0, db_column='board_like_cnt')
    board_dis_cnt = PositiveIntegerField(default = 0, db_column='board_dis_cnt')
    temp_YN = CharField(max_length = 1, db_column='temp_YN')
    view_cnt = PositiveIntegerField(default = 0, db_column='view_cnt')
    user_like = models.ManyToManyField(User, related_name='like_relations')
    user_report = models.ManyToManyField(User, related_name='report_relations')
    
    #외래키
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, db_column='category_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True, db_column='user_id')
    #익명 으로 할거면 board에서 user를 다 지워야한다.
    # 에타같이 로그인이되도 각각의 사용자가 익명으로 작성이되는거 
    # 디씨같이 로그인이 되든안되든 게시글을 올릴떄 익명으로 작성이되는거 (user키를 뺴고 charfile로 board에 새로생성하면되죠?)

    class Meta:
        db_table = 'board'


class Reply(models.Model):
    reply_id=models.AutoField(primary_key=True,db_column='reply_id')
    reply_content=models.CharField(max_length=200,db_column='reply_content',null=False)
    reg_date=DateTimeField(auto_now=True,db_column='reg_date',null=False)
    mod_date=DateTimeField(auto_now=True,db_column='mod_date')
    reply_deleted=CharField(max_length=1, null=False, db_column='reply_deleted')
    reply_like_cnt=models.PositiveIntegerField(default=0, db_column='reply_like_cnt')
    reply_dis_cnt=models.PositiveIntegerField(default=0, db_column= 'reply_dis_cnt')
    #fk
    user=models.ForeignKey(User, on_delete=models.CASCADE, null = False, db_column='user_id', related_name='reply_user_relations')
    board=models.ForeignKey(Board, on_delete=models.CASCADE,null=False, db_column='board_id', related_name='reply_board_relations')

    class Meta:
        db_table = 'reply'

class File(models.Model):
    file_id=AutoField(primary_key=True,db_column='file_id')
    file_name=models.FileField(upload_to='uploads/',db_column='fine_name')
    file_reg_date=DateTimeField(auto_now_add=True,db_column='file_reg_date')
    file_mod_date=DateTimeField(auto_now=True,db_column='file_mod_date')
    file_deleted=CharField(max_length=1,default='N')
    #fk
    board=models.ForeignKey(Board, on_delete=models.CASCADE,null=False, db_column='board_id')

    class Meta:
        db_table = 'file'

class ReplyBookmark(models.Model):
    reg_date = DateTimeField(auto_now_add=True, db_column='reg_date')
    use_YN = CharField(max_length=1, null = False, default = 'Y')
    #fk
    user = models.ForeignKey(User,on_delete = models.CASCADE, null=False, db_column='user_id' )
    reply = models.ForeignKey(Reply, on_delete =models.CASCADE, null=False, db_column='reply_id')


    class Meta:
        db_table = 'reply_bookmark'

class BoardBookmark(models.Model):
    reg_date = DateTimeField(auto_now_add=True, db_column='reg_date')
    use_YN = CharField(max_length=1, null = False, default = 'Y')
    #fk
    user = models.ForeignKey(User,on_delete = models.CASCADE, null=False, db_column='user_id' )
    board = models.ForeignKey(Board, on_delete =models.CASCADE, null=False, db_column='board_id')

    class Meta:
        db_table = 'board_bookmark'

class ReplyLikeReport(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, null=False, db_column='reply_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, db_column='user_id')
    like_YN = models.CharField(max_length=1, null = False)

    class Meta:
        db_table = 'reply_like_report'