from django.urls import path
from authen import views

urlpatterns = [
  path('', views.MyLoginFunc, name='login'),
  path('auth/signup', views.SignUpView.as_view(), name='signup'), 
  path('auth/logout', views.LogoutView.as_view(), name='logout'),
  path('changepassword', views.ChangePassword, name='changepassword'),
  path('password/reset', views.PRView.as_view(), name='password_reset'),
  path('password/reset/done', views.PRDView.as_view(), name='password_reset_done'),
  path('password/reset/confirm/<uidb64>/<token>', views.PRCView.as_view(), name='password_reset_confirm'),
  path('password/reset/complete', views.PRCPView.as_view(), name='password_reset_complete'),
]