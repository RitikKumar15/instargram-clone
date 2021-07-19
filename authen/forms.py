from django import forms
from user.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm

# Sign Up Form Starts Here
class MySignUpForm(UserCreationForm):
  password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}))
  password2 = forms.CharField(label='Confirm Password (again)', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Confirm Password (again)'}))
  class Meta:
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    labels = {'email': 'Email'}
    widgets = {
      'username': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}),
      'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}),
      'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}),
      'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email Address'}),
    }
  
# Login Form Starts Here  
class MyLoginForm(AuthenticationForm):
  username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Username'}))
  password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}))

# Reset Password Form Starts Here
class MyPasswordResetForm(PasswordResetForm):
  email = forms.CharField(widget=forms.EmailInput(attrs={"class":"form-control", "placeholder":"Email"}))
  
# Reset Password Confirm Form Starts Here
class MySetPasswordForm(SetPasswordForm):
  new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'New Password'}))
  new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'New Password Confirm'}))
  
# Password Change Form Starts Here
class MyPasswordChangeForm(PasswordChangeForm):
  old_password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder":"Old Password"}))
  new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder":"New Password"}))
  new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder":"New Password Confirm"}))