from django.urls import path
from django.contrib import admin
from django.urls import include, path
from .views import TaskListView, TaskDetailView, TaskCreateView, TaskDeleteView, TaskUpdateView,TaskSummaryView
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.add_event, name="add_event"),
    path("list/", views.get_events, name="get_events"),
    path("task/list/", TaskListView.as_view(), name="task-list"),
    path("task/new/", TaskCreateView.as_view(), name="task-new"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("task/<int:pk>/edit/", TaskUpdateView.as_view(), name="task-edit"),
    path("task/summary/", TaskSummaryView.as_view(), name="task-summary"),
    
]