from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm
from django.http import HttpRequest
from .models import TaskModel

# Create your views here.
# def tasks_home:
#     return HttpResponse("a")

def tasks_home(request):
    context = {
        "name": "Jamyle",
        "tasks": TaskModel.objects.all()
    }
    return render(request, 'tasks/home.html', context)

def tasks_add(request):
    
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tasks:home")
    context = {
        "form": TaskForm
    }
    return render(request, "tasks/add_tasks.html", context)

def tasks_remove(request:HttpRequest, id):
    task = get_object_or_404(TaskModel, id=id)
    task.delete()
    return redirect("tasks:home")

def tasks_edit(request:HttpRequest, id):
    task = get_object_or_404(TaskModel, id=id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("tasks:home")
    form = TaskForm(instance=task)
    context = {
        "form": form
    }
    return render(request, "tasks/edit_tasks.html", context)

def tasks_mark_completed(request:HttpRequest, id):
    task = get_object_or_404(TaskModel, id=id)
    task.completed = True
    task.save()
    return redirect("tasks:home")