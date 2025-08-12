from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm
from django.http import HttpRequest, HttpResponse
from .models import TaskModel
from accounts.models.user import UserModel
from accounts.models.address import AddressModel
# from users.models import UserModel
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from accounts.views import UserRegistrationChartView
from datetime import date
import json

class TasksAcessMixin(LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'tasks.view_task'
    
    def has_permission(self):
        
        return self.request.user.is_authenticated

def calculate_age(born):
    if born is None:
        return None
    today = date.today()
    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    return age

class TaskListView(LoginRequiredMixin, ListView):
    model = TaskModel
    template_name = 'tasks/tasks_admin.html'
    context_object_name = 'tasks'
    
    def get_queryset(self):
        return TaskModel.objects.filter(user=self.request.user).order_by('-createAt')

class TasksHomeView(LoginRequiredMixin, ListView):
    model = TaskModel
    template_name = 'tasks/home.html'
    context_object_name = 'tasks'
    
    print("=============================UserRegistrationChartView importado:", UserRegistrationChartView)

    def get_queryset(self):
        return TaskModel.objects.filter(user=self.request.user).order_by('-createAt')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        
        COUNTRY_NAMES = {
            "BR": "Brasil",
            "US": "Estados Unidos",
            "PT": "Portugal",
            "FR": "França",
        }
        
        SEX_NAMES = {
            "M": "Masculino",
            "F": "Feminino",
            "O": "Outro",
        }
        
        user_info = AddressModel.objects.filter(usermodel=self.request.user).first()
        context['address'] = user_info
        print(user_info)
        
        
        if user_info:
            context['country_name'] = COUNTRY_NAMES.get(user_info.country, "N/A")
        else:
            context['country_name'] = "N/A"
        
        
        user_tasks = TaskModel.objects.filter(user=self.request.user)
        context['total_tasks'] = user_tasks.count()
        context['completed_tasks'] = user_tasks.filter(completed=True).count()
        context['pending_tasks'] = user_tasks.filter(completed=False).count()
        
        users = UserModel.objects.all()[:10]
        for user in users:
            user.age = calculate_age(user.date_of_birth)
        context['users'] = users
        
        context['name'] = self.request.user.name
        context['sex'] = self.request.user.sex
        context['email'] = self.request.user.email
        
        
        users = UserModel.objects.all().values('id', 'name', 'cpf', 'address__state' ,'sex', 'date_of_birth', 'email')
        users_list = []
        for u in users:
            users_list.append({
                "id": u["id"],
                "name": u["name"],
                "cpf": u["cpf"],
                "address__state": u["address__state"],
                "sex": u["sex"],
                "date_of_birth": u["date_of_birth"].strftime("%Y-%m-%d") if u["date_of_birth"] else None,
                "email": u["email"],
                "age": self.calculate_age(u["date_of_birth"]),
            })

        context['users_json'] = json.dumps(users_list)
        
        chart_view = UserRegistrationChartView()
        chart_context = chart_view.get_context_data(**kwargs)

        context['chart_data'] = chart_context.get('chart_data')
        return context

    def calculate_age(self, born):
        if not born:
            return None
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

class TaskCreateView(LoginRequiredMixin, CreateView): # OK
    model = TaskModel
    template_name = 'tasks/add_tasks.html'
    form_class = TaskForm
    context_object_name = 'task'
    success_url = reverse_lazy('tasks:home')

    def get_queryset(self):
        return TaskModel.objects.filter(user=self.request.user)

    def form_valid(self, form):
        print(f"Usuário logado: {self.request.user} - ID: {self.request.user.id}")
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
