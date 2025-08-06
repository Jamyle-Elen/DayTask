from django.db import models

# Create your models here.
class UserModel(models.Model):
    id = models.CharField(primary_key=True, null=False)
    name = models.CharField(max_length=120, null=False)
    email = models.EmailField(max_length=120, null=False)
    password = models.CharField(max_length=120, null=False)
    createAt = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name