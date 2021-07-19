from django.contrib.auth.models import BaseUserManager
from django.utils.translation import ugettext_lazy as _

class CustomUserManager(BaseUserManager):
  def create_user(self, username, password, **extra_fields):
    if not username:
      raise ValueError(_('The Username Must Be Set.'))
    user = self.model(username=username, **extra_fields)
    user.set_password(password)
    user.save()
    return user

  def create_superuser(self, username, password, **extra_fields):
    extra_fields.setdefault('is_active',True)
    extra_fields.setdefault('is_staff',True)
    extra_fields.setdefault('is_superuser',True)
    
    if extra_fields.get('is_staff') is not True:
      raise ValueError(_('Superuser Must Set To is_staff=True.'))
    if extra_fields.get('is_superuser') is not True:
      raise ValueError(_('Superuser Must Set To is_superuser=True.'))
    return self.create_user(username, password, **extra_fields)