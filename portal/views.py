from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings


# Create your views here.
import json
import urllib
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Profile, Course
from .forms import CoursePageForm, UserForm, ProfileForm, EducationForm, CourseForm
from django.db.models import Q
from .forms import UploadFileForm
# from somewhere import handle_uploaded_file

def loginForm(request):
    if request.method == 'POST':

        ''' Begin reCAPTCHA validation '''
        recaptcha_response = request.POST['g-recaptcha-response']
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req =  urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        ''' End reCAPTCHA validation '''

        if result['success']:
	        username = request.POST['username']
	        password = request.POST['password']
	        user = authenticate(username=username, password=password)
	        if user is not None:
	            if user.is_active:
	                login(request, user)
	                return redirect('/portal/')
	            else:
	                return HttpResponse("Account Disabled.")
	        else:
	        	return render(request, 'registration/login.html', {'error_message': 'Invalid Credentials.'})
        else:
            return render(request, 'registration/login.html', {'error_message': 'Invalid Captcha.'})
    if request.user.is_authenticated:
        return redirect('/portal/')
    else:
        return render(request, 'registration/login.html')


def logoutForm(request):
    logout(request)
    return render(request, 'registration/logout.html')
def adminForm(request):
    return render(request, 'portal/user.html')

def update_profile(request):
    if request.method == 'POST':
        if request.user.profile:
            profile_form = ProfileForm(request.POST,request.FILES,instance=request.user.profile)
        else:
            profile_form = ProfileForm(request.POST,request.FILES)

        if profile_form.is_valid():
            profile_data = profile_form.save(commit=False)
            if not request.user.profile:
                profile_data.user = request.user
            profile_data.save()
            #messages.success(request, _('Your profile was successfully updated!'))
            return redirect('/portal/profile')
        #else:
            #messages.error(request, _('Please correct the error below.'))
    else:
        if request.user.profile:
            profile_form = ProfileForm(instance=request.user.profile)
        else:
            profile_form = ProfileForm()
    return render(request, 'portal/user.html', {
        'profile_form': profile_form
    })

def dashboard(request):
    # # if not request.user.is_authenticated:
    # #     return redirect('/portal/login')
    # if request.method=='POST':
    #     form = CoursePageForm(request.POST,instance=user_data)

    #     if form.is_valid():
    #         user_data = form.save()
    #         user_data.save()
    #         return redirect('/portal/profile/'+str(user))
    # else:
    #     form = CoursePageForm()
    #     return render(request, 'portal/dash.html', {'form':form})
    # return render(request,'portal/dash.html',{'form':form,})
    return render(request,'portal/dash.html')

def addEducation(request):
    if request.method=='POST':
        form = EducationForm(request.POST)
        if form.is_valid:
            eduform=form.save(commit=False)
            eduform.user=request.user
            eduform.save()
            return redirect('/portal/profile')

def list_all_courses(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.user=request.user
            tempuser = Profile.objects.get(user=request.user)
            tempuser.courses = tempuser.courses +1
            if course.active:
                tempuser.active_courses = tempuser.active_courses +1
            tempuser.save()
            course.save()
            return redirect('/portal/courses/')
    else:
        form = CourseForm()
    course = Course.objects.filter(Q(user=request.user) & Q(active=1)).order_by('-startdate')
    incourse = Course.objects.filter(Q(user=request.user) & Q(active=0)).order_by('-enddate')
    return render(request, 'portal/courses.html', {'form': form, 'course':course, 'incourse':incourse,})

def edit_course(request,id):
    if request.method == 'POST':
        form=CourseForm(request.POST)
        if form.is_valid():
            course = Course.objects.get(id=id)
            if course.user.id != request.user.id:
                return HttpResponse('404'+str(request.user)+str(course.user))
            course1=form.save(commit=False)
            course.title=course1.title
            course.course_id=course1.course_id
            course.startdate=course1.startdate
            course.enddate=course1.enddate
            course.semester=course1.semester
            course.url=course1.url
            course.active=course1.active
            course.save()
            return redirect('/portal/courses/')
    return redirect('/portal/courses/')

def delete_course(request,id):
    if request.method == 'POST':
        course = Course.objects.get(id=id)
        if course.user != request.user:
            return HttpResponse('Dont Try To Mess With The System')
        tempuser = Profile.objects.get(user=request.user)
        tempuser.courses = tempuser.courses -1
        if course.active:
            tempuser.active_courses = tempuser.active_courses -1
        tempuser.save()
        course.delete()

        return redirect('/portal/courses/')
    return redirect('/portal/courses/')

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'portal/upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'portal/upload.html')



