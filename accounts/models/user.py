from django.db import models
from .address import AddressModel
from ..choices.sex import SexChoices
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O email deve ser informado")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superusuário precisa ter is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superusuário precisa ter is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class UserModel(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=120, null=False)
    email = models.EmailField(unique=True, max_length=120, null=False)
    cpf = models.CharField(unique=True, max_length=11, null=False)
    date_of_birth = models.DateField(null=True)
    address = models.OneToOneField("AddressModel", on_delete=models.CASCADE, null=True, blank=True)
    sex = models.CharField(max_length=1, choices=SexChoices.choices)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'cpf']
    
    objects = UserManager()

    def __str__(self):
        return self.name