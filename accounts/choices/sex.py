from django.db import models

class SexChoices(models.TextChoices):
    MALE = 'M', 'Masculino'
    FEMALE = 'F', 'Feminino'
    OTHER = 'O', 'Outro'