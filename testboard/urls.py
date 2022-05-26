from django.urls import path
from . import views

#app 이름 설정
app_name= 'testboard' 

urlpatterns = [
    path('', views.base, name = 'test'),
]