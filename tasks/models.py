from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from .choices import TaskPriority
# from accounts.models import UserModel

# Create your models here.
class TaskModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120, null=False)
    description = models.TextField(max_length=120, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    priority = models.CharField(choices=TaskPriority.choices, default=TaskPriority.MEDIUM, null=False)
    createAt = models.DateTimeField(auto_now_add=True, null=False)
    
    def __str__(self):
        return self.name
