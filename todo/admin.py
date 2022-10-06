from django.contrib import admin
from todo.models import Task
from todo.forms import forms
# Register your models here.
admin.site.register(Task) #管理画面でデータを編集したかったらこのようにする
