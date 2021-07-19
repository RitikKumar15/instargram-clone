from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from user.models import User
from .forms import MySignUpForm, MyLoginForm, MyPasswordResetForm, MySetPasswordForm, MyPasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib import messages

# Sign Up View Starts Here
class SignUpView(View):
  def get(self, request):
    form = MySignUpForm()
    return render(request, 'authen/signup.html', {'form':form})
  
  def post(self, request):
    form = MySignUpForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, 'Your Account Created Successful!')
      return redirect('login')
    return render(request, 'authen/signup.html', {'form':form})
    
#Login view function
def MyLoginFunc(request):
  if request.method == 'POST':
    form = MyLoginForm(request=request, data=request.POST)
    if form.is_valid():
      nm = form.cleaned_data.get('username')
      pwd = form.cleaned_data.get('password')
      validUser = authenticate(username=nm, password=pwd)
      if validUser is not None:
        login(request, validUser)
        return redirect('userfeed')
      else:
        return render(request, 'authen/login.html', {'form': form})
  else:
    form = MyLoginForm()
  return render(request, 'authen/login.html', {'form': form})
    
# Change Password Func Starts Here
def ChangePassword(request):
  if request.method == 'POST':
    form = MyPasswordChangeForm(user=request.user, data=request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, 'Your Password Has Been Changed Successful. Login Again')
      return redirect('login')
  else:
    form = MyPasswordChangeForm(request.user)
  return render(request, 'authen/changepassword.html', {'form':form})
    
#Logout View Starts Here
class LogoutView(View):
  def get(self, request):
    logout(request)
    return redirect('login')
  
# Password Reset Starts Here
class PRView(PasswordResetView):
  template_name = 'authen/password_reset.html'
  form_class = MyPasswordResetForm
  
class PRDView(PasswordResetDoneView):
  template_name = 'authen/password_reset_done.html'
  
class PRCView(PasswordResetConfirmView):
  template_name = 'authen/password_reset_confirm.html'
  form_class = MySetPasswordForm
  
class PRCPView(PasswordResetCompleteView):
  template_name = 'authen/password_reset_complete.html'
  
