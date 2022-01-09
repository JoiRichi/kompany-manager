from django.db import models
from .manager import UserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from django.core.exceptions import ObjectDoesNotExist


# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique= True, verbose_name= 'email')
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_counter_staff = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_director = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True



class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=300)
    middle_name = models.CharField(max_length=300, null=True, blank=True)
    last_name = models.CharField(max_length=300)
    address= models.TextField()
    phone_number = models.CharField(max_length=300)

    def __str__(self):
        return "{} {}".format(self.first_name,self.last_name )

