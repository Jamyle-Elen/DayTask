from django.db import models

class TaskPriority(models.TextChoices):
    LOW = 'Low', 'Baixa'
    MEDIUM = 'Medium', 'Média'
    HIGH = 'High', 'Alta'