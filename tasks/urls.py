from django.urls import path
from . import views
from .views import TasksHomeView, tasks_add, tasks_remove, tasks_edit, tasks_mark_completed

app_name = "tasks" #namespace

urlpatterns = [
    # lembrar que quando usa class ao ivnes de function e necessario passar 2 argumentos (views.CLASS_UTILIZADA.as_view())
    path('', TasksHomeView.as_view(), name="home"),
    path('add/', tasks_add, name="add"),
    path('remove/<int:id>', tasks_remove, name="remove"),
    path('edit/<int:id>', tasks_edit, name="edit"),
    path('mark_completed/<int:id>', tasks_mark_completed, name="mark_completed"),
]
