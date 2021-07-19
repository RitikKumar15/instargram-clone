from django import forms
from .models import User
from core.models import Post

# Edit Profile Form Starts Here
class EditProfileForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['picture', 'username', 'first_name', 'last_name', 'email', 'gender', 'phone_number', 'is_private_account']
    labels = {
      'picture':'Change Profile Picture',
      'is_private_account':'Do You Want Make Your Account Private?',
      'phone_number':'Contact Number',
    }
    widgets = {
      'username':forms.TextInput(attrs={'class':'form-control'}),
      'first_name':forms.TextInput(attrs={'class':'form-control'}),
      'last_name':forms.TextInput(attrs={'class':'form-control'}),
      'email':forms.EmailInput(attrs={'class':'form-control'}),
      'gender':forms.Select(attrs={'class':'form-control'}),
      'phone_number':forms.NumberInput(attrs={'class':'form-control'}),
    }
    
# Add Post Form Starts Here
class AddPostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ['image', 'caption']
    labels = {
      'image':'Add Post',
    }
    widgets = {
      'caption':forms.TextInput(attrs={"class":"form-control"})
    }
    