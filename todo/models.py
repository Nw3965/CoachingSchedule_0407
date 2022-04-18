import django
from django.db import models
from django.utils import timezone
from django import forms
class Log(models.Model):
    regist_date = models.DateTimeField(default=timezone.now)

# Create your models here.
class Task(models.Model):
    title = models.CharField('ユーザー名', max_length=30)
    ZoomURL = models.CharField('Zoom URL', max_length=50)
   
    Date = models.DateField('日付',default=django.utils.timezone.now)
    Start = models.DateTimeField('開始時間',default=django.utils.timezone.now)
    deadline = models.DateTimeField('終了時間',default=django.utils.timezone.now) #記入例2022-03-03 00:00:00
    Status = models.CharField('ステータス', max_length=50)
    
    def __str__(self):
        return self.title


######################
class form(forms.Form):
 Date = forms.DateField(input_formats=['%Y/%m/%d'])
 Start = forms.DateTimeField(input_formats=['%Y/%m/%d'])
 deadline = forms.DateTimeField(input_formats=['%Y/%m/%d'])
#####################



#class CoachingUser(models.Model):
#    Username = models.CharField('ユーザー名', max_length=100)
#    UserType = models.IntegerField('ユーザータイプ')
#    ZoomURL = models.TextField('Zoom URL', max_length=50)

#    def __str__(self):
#        return self.Username
