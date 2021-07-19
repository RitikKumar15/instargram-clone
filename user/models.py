from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.utils import timezone

GENDER_CHOICE = (
  ('Male', 'Male'),
  ('Female', 'Female'),
  ('None', 'Prefer Not To Say'),
  )

class User(AbstractUser):
  last_login = models.DateTimeField(default=timezone.now)
  picture = models.ImageField(upload_to='profile_picture', null=True, blank=True)
  gender = models.CharField(choices=GENDER_CHOICE, max_length=10)
  phone_number = models.PositiveIntegerField(null=True, blank=True)
  is_private_account = models.BooleanField(default=False)
  
  USERNAME_FIELD = 'username'
  REQUIRED_FIELD = []
  
   
  objects = CustomUserManager()