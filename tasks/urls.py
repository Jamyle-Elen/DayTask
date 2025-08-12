from django.urls import path
from . import views
from .views import TaskListView, TasksHomeView, TaskCreateView, TaskDeleteView, TaskUpdateView, TaskMarkCompleted

app_name = "tasks" #namespace

urlpatterns = [
    # lembrar que quando usa class ao ivnes de function e necessario passar 2 argumentos (views.CLASS_UTILIZADA.as_view())
    path('', TasksHomeView.as_view(), name="home"),
    path('add/', TaskCreateView.as_view(), name="add"),
    path('delete/<int:pk>', TaskDeleteView.as_view(), name="delete"),
    path('edit/<int:pk>', TaskUpdateView.as_view(), name="edit"),
    path('list', TaskListView.as_view(), name="list"),
    path('mark_completed/<int:pk>', TaskMarkCompleted.as_view(), name="mark_completed"),
]
