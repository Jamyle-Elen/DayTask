from django.db import models

# Create your models here.

class TaskPriority(models.TextChoices):
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'
class TaskModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120, null=False)
    description = models.TextField(max_length=120, null=True, blank=True)
    # user = models.ForeignKey("UserModel", related_name="tasks", null=False, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    priority = models.CharField(choices=TaskPriority.choices, default=TaskPriority.MEDIUM, null=False)
    createAt = models.DateTimeField(auto_now_add=True, null=False)
    
    def __str__(self):
        return self.name
    
    
class UserModel(models.Model):
    id = models.CharField(primary_key=True, null=False)
    name = models.CharField(max_length=120, null=False)
    email = models.EmailField(max_length=120, null=False)
    password = models.CharField(max_length=120, null=False)
    createAt = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name