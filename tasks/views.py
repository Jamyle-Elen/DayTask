from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm
from django.http import HttpRequest, HttpResponse
from .models import TaskModel
from accounts.models import UserModel
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, View
from django.urls import reverse_lazy
from django.contrib import messages

class TasksHomeView(LoginRequiredMixin, ListView):
    model = TaskModel
    template_name = 'tasks/home.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return TaskModel.objects.filter(user=self.request.user).order_by('-createAt')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = self.request.user.first_name or self.request.user.username
        return context

class TaskCreateView(LoginRequiredMixin, CreateView): # OK
    model = TaskModel
    template_name = 'tasks/add_tasks.html'
    form_class = TaskForm
    context_object_name = 'task'
    success_url = reverse_lazy('tasks:home')
    
    def get_queryset(self):
        return TaskModel.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro no envio dos dados, verifique-os")
        return super().form_invalid(form)

class TaskDeleteView(LoginRequiredMixin, DeleteView): #OK
    model = TaskModel
    context_object_name = 'task'
    template_name = 'tasks/taskmodel_confirm_delete.html'
    success_url = reverse_lazy('tasks:home')

class TaskUpdateView(LoginRequiredMixin, UpdateView): #OK
    model = TaskModel
    template_name = 'tasks/edit_tasks.html'
    form_class = TaskForm
    context_object_name = 'task'
    success_url = reverse_lazy('tasks:home')
    
    def get_queryset(self):
        return TaskModel.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao editar dos dados, verifique-os")
        return super().form_invalid(form)

class TaskMarkCompleted(LoginRequiredMixin, View):
    model = TaskModel
    context_object_name = 'task'
    form_class = TaskForm
    sucess_url = reverse_lazy('tasks:home')
    
    def post(self, request, *args, **kwargs):
        task = get_object_or_404(TaskModel, pk=self.kwargs["pk"], user=request.user)
        task.completed = True
        sucess_url = reverse_lazy('tasks:home')
        task.save()
        print("foi")
        return redirect('tasks:home')
