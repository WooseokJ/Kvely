from django import forms
from .models import File,Board
from .models import File

class ReportLikeForm(forms.Form):
    board_id = forms.IntegerField(max_value=None)
    reply_id = forms.IntegerField(max_value=None)
    user_id = forms.IntegerField(max_value=None)
    report_flag = forms.CharField(max_length=1)

class DeleteBoardForm(forms.Form):
    delete_YN = forms.CharField(max_length=1, required=False)
    id = forms.IntegerField(max_value=None)
    board_id = forms.IntegerField(max_value = None)

class ReplyForm(forms.Form):
    board_id = forms.IntegerField(max_value=None)
    user_id = forms.IntegerField(max_value=None)
    reply_content = forms.CharField(max_length=1500, required=True)
