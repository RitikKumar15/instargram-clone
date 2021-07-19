from django.contrib import admin
from .models import (
  Post,
  Comment,
  Like,
  Follow,
  SavedPost,
  )
  
# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
  list_display = ['id', 'user', 'image', 'caption', 'created_on', 'updated_on']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
  list_display = ['id', 'user', 'post', 'text', 'commented_on', 'updated_on']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
  list_display = ['id', 'user', 'post', 'is_liked', 'liked_on', 'updated_on']

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
  list_display = ['id','user', 'is_followed', 'followed', 'followed_on', 'updated_on']
  
@admin.register(SavedPost)
class FollowAdmin(admin.ModelAdmin):
  list_display = ['id','user', 'post', 'saved_on']
  