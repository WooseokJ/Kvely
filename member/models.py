from django.db import models
from django.forms import CharField

# Create your models here.
# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_email = models.EmailField(verbose_name='사용자이메일', unique=True, max_length=50)
    user_pw = models.CharField(max_length=255, null=False)
    user_nick = models.CharField(max_length=30, unique=True)
    user_track = models.CharField(max_length=10, null=False)
    user_class = models.CharField(max_length=10, null=False)
    user_profile = models.CharField(max_length=255)
    
    # fk
    aivle = models.ForeignKey('Aivle', related_name='aivle', on_delete= models.CASCADE, db_column="aivle_id")
    
    class Meta:
        db_table = 'user'
        

class Aivle(models.Model):
    aivle_id = models.AutoField(primary_key = True)
    code = models.CharField(max_length= 8)
    
    class Meta:
        db_table = 'aivle'
        
class Adj(models.Model):
    adj_id = models.AutoField(primary_key=True)
    first = models.CharField(max_length=10, null=False)
    class Meta:
        db_table = 'adj'
            
class Noun(models.Model):
    noun_id = models.AutoField(primary_key = True)
    second = models.CharField(max_length=10, null=False)
    class Meta:
        db_table = 'noun'
    
