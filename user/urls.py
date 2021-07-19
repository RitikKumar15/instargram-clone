from django.urls import path
from user import views

urlpatterns = [
  path('in/<str:username>', views.ProfileView.as_view(), name='profile'),
  path('<str:username>/edit', views.ProfileEditView.as_view(), name='profile_edit'),
  path('search', views.SearchView.as_view(), name='search_view'),
  path('search/details/<int:id>', views.SearchDetailsView.as_view(), name='search_details'),
  path('follow/<int:id>', views.FollowButtonView.as_view(), name='follow'),
  path('unfollow/<int:id>', views.UnFollowButtonView.as_view(), name='unfollow'),
  path('add/post', views.AddPostFunc, name='userposts'),
  path('post/deatils/<int:id>', views.PostDetailsView.as_view(), name='postdetails'),
  path('post/deatils/like/<int:id>', views.PostDetailsLikeView.as_view(), name='postdetailslike'),
  path('delete/post/<int:id>', views.DeletePostView.as_view(), name='deletepost'),
  path('comments', views.CommentPostDetails, name='comments'),
  path('savedposts/<int:id>', views.SavedPostsView.as_view(), name='savedposts'),
  path('user/like', views.UserLikedView.as_view(), name='userliked'),
]