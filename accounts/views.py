# from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView, TemplateView
from django.views.generic.edit import UpdateView, View
from .models.user import UserModel
from .forms.user_form import UserForm
from .models.address import AddressModel
from .forms.address_form import AddressForm
from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
import json
from datetime import date
from django.db.models.functions import TruncDate
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Count
from formtools.wizard.views import SessionWizardView
from django.http import JsonResponse
from django.template.loader import render_to_string

app_name = "accounts"
# Create your views here.
class UserSignUpView(SessionWizardView):
    model = UserModel
    template_name = "registration/signup.html"
    form_list = [
        ("user", UserForm),
        ("address", AddressForm),
    ]
    
    def done(self, form_list, **kwargs):
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)
            
        user = UserModel(
            email=data['email'],
            name=data['name'],
            cpf=data['cpf'],
            date_of_birth=data['date_of_birth'],
            sex=data['sex']
        )
        
        user.set_password(data['password'])
        user.save()
        
        address = AddressModel(
            street=data['street'],
            number=data['number'],
            neighborhood=data['neighborhood'],
            complement=data['complement'],
            city=data['city'],
            state=data['state'],
            postal_code=data['postal_code'],
            country=data['country']
        )
        address.save()

        user.address = address
        user.save()

        return redirect("accounts:signin")

class UserSignInView(LoginView):
    template_name = "registration/signin.html"

class UserLogoutView(LogoutView):
    next_page = 'accounts:signin'

class UsersGridView(UserPassesTestMixin, TemplateView):
    template_name = 'tasks/home.html'
    
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('accounts:signin')

    def calculate_age(self, born):
        if not born:
            return None
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def get_context_data(self, **kwargs):
        print("Entrou no get_context_data")  # vai imprimir a cada requisição

        context = super().get_context_data(**kwargs)

        users = UserModel.objects.all().values('id', 'name', 'sex', 'date_of_birth', 'email')  # corrigido aqui
        print("Queryset users:", list(users))

        users_list = []
        for u in users:
            users_list.append({
                "id": u["id"],
                "name": u["name"],
                "sex": u["sex"],
                "date_of_birth": u["date_of_birth"].strftime("%Y-%m-%d") if u["date_of_birth"] else None,
                "email": u["email"],
                "age": self.calculate_age(u["date_of_birth"])
            })

        print("Users list montada:", users_list)

        return context

class UserRegistrationChartView(UserPassesTestMixin,TemplateView):
    template_name = 'metrics/components/chart_line_base.html'
    
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('accounts:signin')

    print("Vai entrar no get_context_data")
    def get_context_data(self, **kwargs):
        print("Entrou no get_context_data")
        context = super().get_context_data(**kwargs)
        chart_data_qs = (
            UserModel.objects
            .annotate(date=TruncDate('created_at'))
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )

        dates = [str(d['date']) for d in chart_data_qs]
        counts = [d['count'] for d in chart_data_qs]

        context['chart_data'] = json.dumps(dates)
        context['chart_data'] = json.dumps(counts)

        print("===============",chart_data_qs)
        return context

class MetricsView(UserPassesTestMixin, TemplateView):
    template_name = 'metrics/metrics.html'
    
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('accounts:signin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # gênero para gráfico de rosca
        gender_counts = UserModel.objects.values('sex').annotate(count=Count('sex'))
        counts = {'F': 0, 'M': 0, 'O': 0}
        for item in gender_counts:
            key = item['sex']
            if key in counts:
                counts[key] = item['count']

        labels_gender = ['Feminino', 'Masculino', 'Outros']
        values_gender = [counts['F'], counts['M'], counts['O']]

        # estado pra gráfico de barras
        state_counts = UserModel.objects.values('address__state').annotate(count=Count('id')).order_by('address__state')
        labels_state = [item['address__state'] for item in state_counts if item['address__state'] and item['address__state'] != 'Desconhecido' and item['address__state'] != 'N/A' and item['address__state'] != 'Desconhecido']
        values_state = [item['count'] for item in state_counts]
        
        # cidadoes pra grático de barras
        city_counts = UserModel.objects.values('address__city').annotate(count=Count('id')).order_by('address__city')
        labels_city = [item['address__city'] for item in city_counts if item['address__city'] and item['address__city'] != 'Desconhecido' and item['address__city'] != 'N/A' and item['address__city'] != 'Desconhecido']
        values_city = [item['count'] for item in city_counts]

        context['labels_gender'] = json.dumps(labels_gender)
        context['values_gender'] = json.dumps(values_gender)

        context['labels_state'] = json.dumps(labels_state)
        context['values_state'] = json.dumps(values_state)
        
        context['labels_city'] = json.dumps(labels_city)
        context['values_city'] = json.dumps(values_city)

        return context

class UserUpdateView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('accounts:signin')

    def get(self, request, pk, *args, **kwargs):
        user = get_object_or_404(UserModel, pk=pk)
        address = getattr(user, 'addressmodel', None)

        if request.GET.get('modal'):
            user_form = UserForm(instance=user)
            address_form = AddressForm(instance=address)
            html = render_to_string('users/user_update.html', {
                'user_form': user_form,
                'address_form': address_form,
                'user': user,
            }, request=request)
            return JsonResponse({'html_form': html})

        return redirect('tasks:home')

    def post(self, request, pk, *args, **kwargs):
        user = get_object_or_404(UserModel, pk=pk)
        address = getattr(user, 'addressmodel', None)

        user_form = UserForm(request.POST, instance=user)
        address_form = AddressForm(request.POST, instance=address)

        if user_form.is_valid() and address_form.is_valid():
            user_form.save()
            address_form.save()
            if (request.headers.get('x-requested-with') == 'XMLHttpRequest') or request.GET.get('modal'):
                return JsonResponse({'success': True})
            return redirect('tasks:home')
        else:
            if (request.headers.get('x-requested-with') == 'XMLHttpRequest') or request.GET.get('modal'):
                html = render_to_string('users/user_update_modal.html', {
                    'user_form': user_form,
                    'address_form': address_form,
                    'user': user,
                }, request=request)
                return JsonResponse({'success': False, 'html_form': html})
            # fallback
            return redirect('tasks:home')

class UserDeleteView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return JsonResponse({"error": "Permissão negada"}, status=403)

    def post(self, request, pk, *args, **kwargs):
        user = get_object_or_404(UserModel, pk=pk)
        user.delete()
        return JsonResponse({"success": True})
