from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm
from django.http import HttpRequest
from .models import TaskModel
from accounts.models import UserModel
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

# Create your views here.

# @login_required
# def tasks_home(request):
#     tasks = TaskModel.objects.filter(user=request.user)
#     context = {
#         "tasks": tasks,
#         "name": request.user.first_name or request.user.username,
#     }
#     return render(request, 'tasks/home.html', context)

# to study
# comparado com a funçao de cima, usar CBV's ajuda a reaproveitar o codigo e nele tem algumas funções prontas (genericas)
# @login_required       em classes não se usa o decorador @login_required, pq se não força ele a ter o comportamento de uma função e não uma classe
class TasksHomeView(LoginRequiredMixin ,ListView):
    model = TaskModel
    template_name = 'tasks/home.html'  # template utilizado
    context_object_name = 'tasks'  # nome da variável no template

    def get_queryset(self):
        # Filtra as tarefas do usuário logado
        return TaskModel.objects.filter(user=self.request.user).order_by('-createAt')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # adiciona o nome do usuário ao contexto
        context['name'] = self.request.user.first_name or self.request.user.username
        return context

# --------------------------------

@login_required
def tasks_add(request):
    
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect("tasks:home")
    context = {
        "form": TaskForm
    }
    return render(request, "tasks/add_tasks.html", context)

def tasks_remove(request:HttpRequest, id):
    task = get_object_or_404(TaskModel, id=id)
    task.delete()
    return redirect("tasks:home")

@login_required
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