from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.contrib.auth import get_user_model, login
from .forms import EditProfileForm, AddPostForm
from django.contrib import messages
from .models import User
from core.models import Follow, Post, Like, Comment, SavedPost
from django.db.models import Q, Count
from django.urls import reverse

# Profile View Starts Here
class ProfileView(View):
  def get(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      username = kwargs.get('username')
      follow_count = User.objects.get(username=username).follow_user.count()
      following_count = User.objects.get(username=username).follow_followed.count()
      post_count = Post.objects.filter(user__username=request.user.username).count()
      curr_user_posts = Post.objects.all().filter(user=request.user)
      savedposts = SavedPost.objects.all().filter(user__username=username)
      if username == request.user.username:
        return render(request, 'user/profile.html', {'follow_count':follow_count, 'following_count':following_count, 'curr_user_posts':curr_user_posts, 'post_count':post_count, 'savedposts':savedposts})
      try:
        user = get_user_model().objects.get(username=username)
        user_id = user.id
        anon_user_posts = Post.objects.all().filter(user__username=username)
        follow_count = user.follow_user.count()
        following_count = user.follow_followed.count()
        post_count = Post.objects.filter(user__username=username).count()
        follows = Follow.objects.all().filter(user__username=request.user.username)
        is_follow = False
        for f in follows:
          get_id = f.followed.id
          get_user = User.objects.get(pk=get_id).username
          print(f"get_user {get_user} username {username}")
          if get_user == username:
            is_follow = True
            break
          else:
            is_follow = False
      except:
        return HttpResponse('Such Page Does Not Exists!')
      context = {'user':user, 'follow_count':follow_count, 'following_count':following_count, 'is_follow':is_follow, 'anon_user_posts':anon_user_posts, 'post_count':post_count}
      return render(request, 'user/anon_profile.html', context)
    else:
      return redirect('login')

# Profile Edit View Starts Here
class ProfileEditView(View):
  def get(self, request, *args, **kwargs):
    username = kwargs.get('username')
    if username != request.user.username:
      return HttpResponse('Such Page Does Not Exist!')
    form = EditProfileForm(instance=request.user)
    return render(request, 'user/profile_edit.html', {'form':form})
    
  def post(self, request, *args, **kwargs):
    form = EditProfileForm(request.POST, request.FILES, instance=request.user)
    if form.is_valid():
      form.save()
      messages.success(request, 'Data Updated Successful!')
      return redirect('profile_edit', request.user.username)
    form = EditProfileForm(instance=request.user)
    return render(request, 'user/profile_edit.html', {'form':form})
  
# Search View Starts Here
class SearchView(View):
  def get(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      search = request.GET.get('search')
      all_profiles = User.objects.all().filter(first_name__icontains=search).exclude(first_name=request.user.first_name)
      return render(request, 'user/all_profiles.html', {'all_profiles':all_profiles, 'check':False})
    else:
      return redirect('login')
    
#Search Details View Starts Here
class SearchDetailsView(View):
  def get(self, request, id):
    if request.user.is_authenticated:
      try:
        user = User.objects.get(pk=id)
        username = user.username
        if username == request.user.username:
          return HttpResponse('No Results Found!')
        follow_count = User.objects.get(pk=id).follow_user.count()
        following_count = User.objects.get(pk=id).follow_followed.count()
        post_count = Post.objects.filter(user__username=username).count()
        anon_user_posts = Post.objects.all().filter(user__username=username)
        follows = Follow.objects.all().filter(user__username=request.user.username)
        is_follow = False
        for f in follows:
          get_id = f.followed.id
          get_user = User.objects.get(pk=get_id).username
          print(f"get_user {get_user} username {username}")
          if get_user == username:
            is_follow = True
            break
          else:
            is_follow = False
        context = {'user':user, 'follow_count':follow_count, 'following_count':following_count, 'is_follow':is_follow, 'post_count':post_count, 'anon_user_posts':anon_user_posts}
      except:
        return HttpResponse('No Results Found!')
      return render(request, 'user/anon_profile.html', context)
    else:
      return redirect('login')
    
# Follow Button View Starts Here
class FollowButtonView(View):
  def get(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      user_id = kwargs.get('id')
      user = User.objects.get(pk=user_id)
      user_name = User.objects.get(pk=user_id).username
      Follow(followed=user).save()
      return redirect('profile', username=user_name)
    else:
      return redirect('login')
    
#Unfollow Button View Starts Here
class UnFollowButtonView(View):
  def get(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      user_id = kwargs.get('id')
      print(user_id)
      user = User.objects.get(pk=user_id)
      print(user)
      user_name = User.objects.get(pk=user_id).username
      f = Follow.objects.get(user=request.user.id, followed=user_id)
      f.delete()
      return redirect('profile', username=user_name)
    else:
      return redirect('login')
    
#Add Post Function Starts Here
def AddPostFunc(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
      form = AddPostForm(request.POST, request.FILES)
      if form.is_valid():
        image = form.cleaned_data.get('image')
        caption = form.cleaned_data.get('caption')
        Post(image=image, caption=caption).save()
        username = request.user.username
        messages.success(request, 'Post Has Been Uploaded Successfully!')
        return redirect('profile', username=username)
    else:
      form = AddPostForm()
      return render(request, 'user/addpost.html', {'form':form})
  else:
    return redirect('login')
    
#Post details View Start Here
class PostDetailsView(View):
  def get(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      post_id = kwargs.get('id')
      post_user = request.user.id
      post_details = Post.objects.get(pk=post_id)
      liked_or_not = False
      saved_or_not = False
      if SavedPost.objects.filter(Q(post=post_id) & Q(user=post_user)).exists():
        saved_or_not = True
      if Like.objects.filter(Q(post=post_id) & Q(user=post_user)).exists():
        liked_or_not = True
      like_count = Like.objects.all().filter(post__pk=post_id).count()
      comment_count = Comment.objects.all().filter(post=post_id).count()
      comments = Comment.objects.all().filter(post=post_id)
      username = request.user.username
      return render(request, 'user/postdetails.html', {'post_details':post_details, 'like_count':like_count, 'username':username, 'comments':comments, 'comment_count':comment_count, 'liked_or_not':liked_or_not, 'saved_or_not':saved_or_not})
    else:
      return redirect('login')
    
# Post Detail Like & UnLike View Starts Here 
class PostDetailsLikeView(View):
  def get(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      post_id = kwargs.get('id')
      post_user = request.user.id
      post_inst = Post.objects.get(pk=post_id)
      user_inst = User.objects.get(pk=post_user)
      if Like.objects.filter(Q(post=post_id) & Q(user=post_user)).exists():
        l = Like.objects.get(post=post_id, user=post_user)
        l.delete()
        like_count = Like.objects.all().filter(post__pk=post_id).count()
        return redirect('postdetails', id=post_id) 
      Like(post=post_inst, user=user_inst).save()
      like_count = Like.objects.all().filter(post__pk=post_id).count()
      return redirect('postdetails', id=post_id)
    else:
      return redirect('login')
    
#Delete Post View starts Here
class DeletePostView(View):
  def get(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      post_id = kwargs.get('id')
      p = Post.objects.get(pk=post_id)
      p.delete()
      username = request.user.username
      messages.success(request, 'Post Has Been Deleted Successful!')
      return redirect('profile', username=username)
    else:
      return redirect('login')
    
#Comment Post Details Func Start Here
def CommentPostDetails(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
      post_id = request.POST.get('post_id')
      text = request.POST.get('comment')
      #post_user = Post.objects.get(pk=post_id).user.id
      post_inst = Post.objects.get(pk=post_id)
      #user_inst = User.objects.get(pk=post_user)
      if text != '':
        Comment(post=post_inst, text=text).save()
        return redirect('postdetails', id=post_id)
    return redirect('postdetails', id=post_id)
  else:
    return redirect('login')
  
# Post Saved View Starts Here
class SavedPostsView(View):
  def get(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      post_id = kwargs.get('id')
      user_id = request.user.id
      if not SavedPost.objects.all().filter(post=post_id).exists():
        s = SavedPost(post_id=post_id )
        s.save()
        return redirect('postdetails', id=post_id)
      s = SavedPost.objects.get(post=post_id)
      s.delete()
      return redirect('postdetails', id=post_id)
    else:
      return redirect('login')
    
# Current User Like View Starts Here
class UserLikedView(View):
  def get(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      liked = Like.objects.all().filter(user_id=request.user.id)
      return render(request, 'user/userliked.html', {'liked':liked}) 
    else:
      return redirect('login')  