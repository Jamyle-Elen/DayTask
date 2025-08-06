from django.urls import path
from . import views

app_name = "tasks" #namespace

urlpatterns = [
    path('', views.tasks_home, name="home"),
    path('add/', views.tasks_add, name="add"),
    path('remove/<int:id>', views.tasks_remove, name="remove"),
    path('edit/<int:id>', views.tasks_edit, name="edit"),
    path('mark_completed/<int:id>', views.tasks_mark_completed, name="mark_completed"),
]
