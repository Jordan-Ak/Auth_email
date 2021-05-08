from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from accounts.managers import CustomUserManager
from common.models import BaseModel
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class CustomUser(AbstractUser, BaseModel):
    """
   Custom User Model
    """
    username = None
    date_joined = None
    first_name = models.CharField(_('first name'), max_length=150,)
    last_name = models.CharField(_('last name'), max_length=150,)
    email = models.EmailField(_('email address'), blank=False, unique = True)
    phone_no = PhoneNumberField(_('phone number'),unique = True,) 
    password_last_changed = models.DateTimeField(_('password last changed'), null=True)
    is_verified = models.BooleanField(_('is verified'), default = False,)
    
    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','phone_no',]

    def __str__(self) -> str:
        return self.email