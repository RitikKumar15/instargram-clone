from django.urls import path
from core import views


urlpatterns = [
  path('user/feed', views.UserFeedView.as_view(), name='userfeed'),
] 