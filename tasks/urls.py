from django.urls import path
from . import views

app_name = "tasks" #namespace

urlpatterns = [
    path('', views.tasks_home),
    path('add/', views.tasks_add, name="add"),
]
