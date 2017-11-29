from django import forms

# from .models import ForumPost, Comment, Messages, PostCategory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.files.images import get_image_dimensions
from django.forms import ModelForm
from .models import *

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'designation', 'office', 'residence', 'phone', 'webmail', 'avatar')

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        try:
            w, h = get_image_dimensions(avatar)

            #validate dimensions
            max_width = max_height = 2000
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                     '%s x %s pixels or smaller.' % (max_width, max_height))

            #validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg','jpg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                    'GIF or PNG image.')

            #validate file size
            if len(avatar) > (4000 * 1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 20k.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar

class CoursePageForm(ModelForm):
    class Meta:
        model = CoursePage
        fields = '__all__'

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ('degree','desc','institute','year')

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title','pi','copi','funding','startyear','endyear')

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('course_id','title','startdate','enddate','url','semester','active')

class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ('authors','title','journal')

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('name','degree','thesis_title','supervisors','completed')

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class LinkForm(forms.Form):
    link=forms.URLField(required=True)
    class Meta:
        fields=('link')

class QueryForm(forms.Form):
    name=forms.CharField(required=True)
    email=forms.EmailField(required=True)
    subject=forms.CharField(required=True)
    message=forms.CharField(required=True)
    class Meta:
        fields=('name', 'email', 'subject', 'message')

class NewUserForm(forms.Form):
    email=forms.EmailField(required=True)
    username=forms.CharField(required=True)
    name=forms.CharField(required=True)
    class Meta:
        fields = ('email', 'username', 'name')

class SignUpForm(UserCreationForm):
    username=forms.CharField(max_length=60,required=True, widget=forms.TextInput(attrs={'class':'form-control',}))
    email=forms.EmailField(max_length=100, required=True, widget=forms.TextInput(attrs={'class':'form-control',}))
    password1=forms.CharField(max_length=100, label='Password',required=True, widget=forms.PasswordInput(attrs={'class':'form-control',}))
    password2=forms.CharField(max_length=100,label='Retype Password', required=True, widget=forms.PasswordInput(attrs={'class':'form-control',}))
    #birth_date=forms.DateField(widget=forms.TextInput(attrs={'id':'datepicker','class':'form-control',}))
    class Meta:
        model = User
        fields=('username','email','password1','password2',)
