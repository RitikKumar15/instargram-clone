from django.db import models
from user.models import User
from crum import get_current_user

# Post Model
class Post(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
  image = models.ImageField(upload_to='post_image', null=True, blank=True)
  caption = models.CharField(max_length=200)
  created_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return str(self.id)
    
  def save(self, *args, **kwargs):
    user = get_current_user()
    if user and not user.pk:
      user = None
    if not self.pk:
      self.user = user
      super(Post, self).save(*args, **kwargs)
  
# Comment Model
class Comment(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  text = models.CharField(max_length=200)
  commented_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return self.text
    
  def save(self, *args, **kwargs):
    user = get_current_user()
    if user and not user.pk:
      user = None
    if not self.pk:
      self.user = user
      super(Comment, self).save(*args, **kwargs)
  
# Like Model
class Like(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  is_liked = models.BooleanField(default=True)
  liked_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return self.is_liked
  
# Follow Model
class Follow(models.Model):
  user = models.ForeignKey(User, related_name='follow_user', on_delete=models.CASCADE, editable=False)
  followed = models.ForeignKey(User, related_name='follow_followed', on_delete=models.CASCADE)
  is_followed = models.BooleanField(default=False)
  followed_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return f"{self.user} Follow {self.followed}"
    
  def save(self, *args, **kwargs):
    user = get_current_user()
    if user and not user.pk:
      user = None
    if not self.pk:
      self.user = user
      super(Follow, self).save(*args, **kwargs)
      
class SavedPost(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  saved_on = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return str(self.id)
    
  def save(self, *args, **kwargs):
    user = get_current_user()
    if user and not user.pk:
      user = None
    if not self.pk:
      self.user = user
      super(SavedPost, self).save(*args, **kwargs)