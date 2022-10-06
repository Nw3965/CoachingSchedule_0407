import django
from django.db import models
from django.utils import timezone
from django import forms
#class Log(models.Model):
 #   regist_date = models.DateTimeField(default=timezone.now)


# Create your models here.
class Task(models.Model):
    YOTEI = '予定'
    JISSEKI = '実績'
    SKIP = 'スキップ'
    STATUS_CHOICES =[
        #左がデータベースに格納される文字列、右がWebページに表示される文字列
        (YOTEI, '予定'),
        (JISSEKI, '実績'),
        (SKIP, 'スキップ'),
    ]

    title = models.CharField('ユーザー名', max_length=30)
    ZoomURL = models.URLField('Zoom URL', max_length=256)
    #Date = models.DateField('日付',default=django.utils.timezone.now) #消す
    Start = models.TimeField('開始時間',default=django.utils.timezone.now)
    deadline = models.TimeField('終了時間',default=django.utils.timezone.now) #記入例2022-03-03 00:00:00
   
    Status = models.CharField(
        'ステータス',
        max_length=16,
        choices=STATUS_CHOICES,
        default=YOTEI,
    )
    start_date = models.DateField('開始日',null=True)
    end_date = models.DateField('終了日',null=True)
    #link = models.URLField(max_length = 200)
    eventid = models.CharField('イベントID', max_length=26,null=True)
    
    def __str__(self):
       return self.title

# class Event(models.Model):
#     start_date = models.DateField()
#     end_date = models.DateField()
#     event_name = models.CharField(max_length=200)



#class CoachingUser(models.Model):
#    Username = models.CharField('ユーザー名', max_length=100)
#    UserType = models.IntegerField('ユーザータイプ')
#    ZoomURL = models.TextField('Zoom URL', max_length=50)

#    def __str__(self):
#        return self.Username
