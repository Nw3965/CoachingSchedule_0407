from itertools import count
from turtle import title
from urllib import request
from django import forms
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from todo.forms import TaskCreateform, TaskUpdateform 

from todo.models import Task
from django.views.generic.edit import FormView
from todo.forms import forms
import json
from .models import Task
from .forms import EventForm
from django.http import Http404
import time
from django.template import loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.middleware.csrf import get_token
from django.http import JsonResponse
from .forms import CalendarForm
from django.db.models import Count
import logging
import datetime, re
import googleapiclient.discovery
import google.auth
import datetime

# 編集スコープの設定(今回は読み書き両方OKの設定)
SCOPES = ['https://www.googleapis.com/auth/calendar']
# カレンダーIDの設定(基本的には自身のgmailのアドレス)
calendar_id = '**********@group.calendar.google.com'
    
# 認証ファイルを使用して認証用オブジェクトを作成
gapi_creds = google.auth.load_credentials_from_file('exalted-airfoil-353804-a78bd1f01ef2.json', SCOPES)[0]
    
# 認証用オブジェクトを使用してAPIを呼び出すためのオブジェクト作成
service = googleapiclient.discovery.build('calendar', 'v3', credentials=gapi_creds)
logging.basicConfig(level=logging.DEBUG)

# Create your views here.
class TaskListView(LoginRequiredMixin,ListView):
    model = Task
    template_name = "todo/task_list.html"
    def get_queryset(self):
        qs = super(TaskListView, self).get_queryset()
       # qs = qs.filter(title=self.request.user) # クッキーの中のユーザー名を取ってくる。データベースからログイン中のユーザー一致する名前だけとってくる。直近一週間など
        dt=datetime.datetime.now()
        if self.request.user.is_superuser:
            qs = Task.objects.filter(start_date__month=dt.month,start_date__year=dt.year).order_by('title','start_date','Status')
        else:
            qs = Task.objects.filter(start_date__month=dt.month,start_date__year=dt.year,title=self.request.user.username,).order_by('title')
            


        return qs

class TaskSummaryView (LoginRequiredMixin,ListView):
    model = Task
    template_name = "todo/task_summary.html"
    def get_queryset(self):
        qs = super(TaskSummaryView, self).get_queryset()
        dt=datetime.datetime.now()
        if self.request.user.is_superuser:
            qs = Task.objects.filter(start_date__month=dt.month,start_date__year=dt.year,Status='スキップ').values('title').annotate(count=Count('Status'))
        else:
            qs = Task.objects.filter(start_date__month=dt.month,start_date__year=dt.year,title=self.request.user.username,Status='スキップ').values('title').annotate(count=Count('Status'))
        logging.debug("件数:{}".format(qs.count()))
        return qs


    # def get_queryset(self):
    #     qs = super(TaskListView, self).get_queryset()
    #     qs = qs.filter(start_date=self) # 
    #     return qs
        
    # def get_queryset(self):
    #     qs = super(TaskListView, self).get_queryset()
    #     qs = qs.filter(end_date=self) # 
    #     return qs


class TaskDetailView(LoginRequiredMixin,DetailView):
    model = Task
    template_name = "todo/task_detail.html"


class TaskCreateView(LoginRequiredMixin,CreateView):
    #print(self.user) ここにGoogleカレンダー登録？
    model = Task
    form_class = TaskCreateform
    

    def form_valid(self, form):
        post = form.save(commit=False)
    
        #tmpを30分未満で切り捨てる処理 datetime.replace 
      
        if post.Start.minute>=30:
            post.Start= post.Start.replace(minute=30,second=0)
        else:
            post.Start= post.Start.replace(minute=0,second=0)

        dt = datetime.datetime(2022, 1, 1)
        t1 = datetime.datetime.combine(dt,post.Start)
        t2= t1+ datetime.timedelta(minutes=30)
        post.deadline= post.Start.replace(hour=t2.hour,minute=t2.minute,second=t2.second)
       
        
        logging.debug(post.deadline)
        post.end_date = post.start_date
        post.save()
# ②予定を書き込む
# 書き込む予定情報を用意する
        s=datetime.datetime(
            post.start_date.year,
            post.start_date.month,
            post.start_date.day,
            post.Start.hour,
            post.Start.minute
        )


        e=datetime.datetime(
            post.end_date.year,
            post.end_date.month,
            post.end_date.day,
            post.deadline.hour,
            post.deadline.minute
        )
        
        event = {
            # 予定のタイトル
            'summary': post.title,
            # 予定の開始時刻
            'start': {
                'dateTime':  s.isoformat(),
                'timeZone': 'Asia/Tokyo'
            },
            # 予定の終了時刻
            'end': {
                'dateTime': e.isoformat(),
                'timeZone': 'Asia/Tokyo'
            },
        }
        # 用意した予定を登録する event id を djanboのDBに登録
        logging.debug(event)
        event = service.events().insert(calendarId=calendar_id, body=event).execute()
        logging.debug(event)
        post.eventid = event['id']
        post.save()
        return HttpResponseRedirect(reverse_lazy("index"))


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("index")
    template_name = "todo/task_delete.html"
            
    # djangoのカレンダーの予定の削除 
    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        
        # Googleカレンダーのイベント削除
        logging.debug(self.object)
        event = service.events().delete(calendarId=calendar_id, eventId= self.object.eventid).execute()
        logging.debug(event)
        return HttpResponseRedirect(reverse_lazy("index"))


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    form_class = TaskUpdateform
    model = Task
    #fields = "__all__"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        post = form.save(commit=False)
    
        #tmpを30分未満で切り捨てる処理 datetime.replace 
      
        if post.Start.minute>=30:
            post.Start= post.Start.replace(minute=30,second=0)
        else:
            post.Start= post.Start.replace(minute=0,second=0)

        dt = datetime.datetime(2022, 1, 1)
        t1 = datetime.datetime.combine(dt,post.Start)
        t2= t1+ datetime.timedelta(minutes=30)
        post.deadline= post.deadline.replace(second=0)
   
        logging.debug(post.deadline)
        post.end_date = post.start_date
        post.save()
   
    # ②予定を書き込む
    # 書き込む予定情報を用意する
        s=datetime.datetime(
            post.start_date.year,
            post.start_date.month,
            post.start_date.day,
            post.Start.hour,
            post.Start.minute
        )


        e=datetime.datetime(
            post.end_date.year,
            post.end_date.month,
            post.end_date.day,
            post.deadline.hour,
            post.deadline.minute
        )
        
        event = {
            # 予定のタイトル
            'summary': post.title,
            # 予定の開始時刻
            'start': {
                'dateTime':  s.isoformat(),
                'timeZone': 'Asia/Tokyo'
            },
            # 予定の終了時刻
            'end': {
                'dateTime': e.isoformat(),
                'timeZone': 'Asia/Tokyo'
            },
        }

        # 用意した予定を登録する
        logging.debug(event)
        event = service.events().update(calendarId=calendar_id, body=event ,eventId= post.eventid).execute()
        logging.debug(event)
        return HttpResponseRedirect(reverse_lazy("index"))



def add_event(request):
    """
    イベント登録
    """

    if request.method == "GET":
        # GETは対応しない
        raise Http404()

    # JSONの解析
    datas = json.loads(request.body)

    logging.debug(datas)

    # バリデーション
    eventForm = EventForm(datas)
    if eventForm.is_valid() == False:
        # バリデーションエラー
        raise Http404()

    # リクエストの取得
    start_date = datas["start_date"]
    end_date = datas["start_date"]
    title = datas["title"]
    status = datas["title"]

    # 日付に変換。JavaScriptのタイムスタンプはミリ秒なので秒に変換
    formatted_start_date = time.strftime(
        "%Y-%m-%d", time.localtime(start_date / 1000))
    formatted_end_date = time.strftime(
        "%Y-%m-%d", time.localtime(end_date / 1000))

    # 登録処理
    event = Task(
        title=str(title),
        start_date=formatted_start_date,
        end_date=formatted_end_date,
        status=str(status),
    )
    event.save()

    # 空を返却
    return HttpResponse("")
    
     # トップ画面
def index(request):
    """
    カレンダー画面
    """
    # CSRFのトークンを発行する
    get_token(request)

    template = loader.get_template("todo/index.html")
    return HttpResponse(template.render())
    
def get_events(request):

    """
    イベントの取得
    """

    if request.method == "GET":
        # GETは対応しない GETは表示 URL手で打つ時　POSTはデータ登録
        raise Http404()

    # JSONの解析
    datas = json.loads(request.body)

    # バリデーション
    calendarForm = CalendarForm(datas)
    if calendarForm.is_valid() == False:
        # バリデーションエラー
        raise Http404()

    # リクエストの取得
    start_date = datas["start_date"]
    end_date = datas["end_date"]

    # 日付に変換。JavaScriptのタイムスタンプはミリ秒なので秒に変換
    formatted_start_date = time.strftime(
        "%Y-%m-%d", time.localtime(start_date / 1000))
    formatted_end_date = time.strftime(
        "%Y-%m-%d", time.localtime(end_date / 1000))

    # FullCalendarの表示範囲のみ表示
    if not request.user.is_superuser:
        events = Task.objects.filter(
            start_date__lt=formatted_end_date, end_date__gt=formatted_start_date,title=request.user.username   
        )
    else:
        events = Task.objects.filter(
            start_date__lt=formatted_end_date, end_date__gt=formatted_start_date  
        )

    # fullcalendarのため配列で返却 　　　開始時刻などを足してカレンダーに表示する
    list = []
    for event in events:
        list.append(
            {# title 後ろの文字列が表示される。#6/16 ステータスはプルダウンメニューにする。
                "title": "{}さん　{}から {}".format(event.title, event.Start,event.Status),
                "status": "{}".format(event.Status),
                "start": event.start_date,
                "id": event.id,
                "end": event.end_date,
                #"end": event.end_date, -> "end": event.start_date,
                #削除ボタンの追加-> 作成済みのタスクをクリックすると削除ページに飛ぶ。http://127.0.0.1:8000/task/4/delete/  ->　http://127.0.0.1:8000/task/{}/delete/
            }
        )

    return JsonResponse(list, safe=False)
