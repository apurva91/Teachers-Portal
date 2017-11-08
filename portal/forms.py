from django import forms

# from .models import ForumPost, Comment, Messages, PostCategory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# class PostForm(forms.ModelForm):
# 	topic = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
# 	#text = forms.CharField(widget=forms.Textarea(attrs={'rows':'5', 'cols':'50','class':'form-control'}))
# 	class Meta:
# 		model = ForumPost
# 		fields = ('topic', 'text','category')

# class SignUpForm(UserCreationForm):
# 	username=forms.CharField(max_length=60,required=True, widget=forms.TextInput(attrs={'class':'form-control',}))
# 	first_name=forms.CharField(max_length=25,required=True, widget=forms.TextInput(attrs={'style':'text-transform:capitalize;','class':'form-control',}))
# 	last_name=forms.CharField(max_length=25, required=True, widget=forms.TextInput(attrs={'style':'text-transform:capitalize;','class':'form-control',}))
# 	email=forms.EmailField(max_length=100, required=True, widget=forms.TextInput(attrs={'class':'form-control',}))
# 	password1=forms.CharField(max_length=100, label='Password',required=True, widget=forms.PasswordInput(attrs={'class':'form-control',}))
# 	password2=forms.CharField(max_length=100,label='Retype Password', required=True, widget=forms.PasswordInput(attrs={'class':'form-control',}))
# 	#birth_date=forms.DateField(widget=forms.TextInput(attrs={'id':'datepicker','class':'form-control',}))
# 	class Meta:
# 		model = User
# 		fields=('username','first_name','last_name','email','password1','password2',)
