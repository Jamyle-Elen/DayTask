from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# def tasks_home:
#     return HttpResponse("a")

def tasks_home(request):
    context = {
        "name": "Jamyle"
    }
    return render(request, 'tasks/home.html', context)

def tasks_add(request):
    return HttpResponse("Adicionar tasks")