from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import json
import urllib
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from portal.models import Profile,Course,Education
from django.views import generic
from django.db.models import Q
from django.contrib.auth.models import User
from portal.forms import *
from portal.models import *
def index(request):
	return render(request, 'index.html')

def faculty(request):
	users = Profile.objects.all()
	return render(request,'faculty.html',{'users':users})
# class IndexView(generic.ListView):
#     model = Profile
#     template_name = 'index.html'
#     context_object_name = 'all_items'

	# def get_queryset(self):
    #     return Profile.objects.all()

# def fac_home(request, pk):
# 	fac = Profile.objects.get(pk=pk)
# 	context = {'fac' : fac}
# 	return render(request, 'homepage.html', context)

def teacher(request,username):
	user = Profile.objects.get(user__username=username)
	suc_message=""
	error_message=''
	course=Course.objects.filter(Q(active=True) & Q(user=user.user.id)).order_by('-semester')
	incourse=Course.objects.filter(Q(active=False) & Q(user=user.user.id)).order_by('-semester')
	education=Education.objects.filter(Q(user=user.user.id)).order_by('-year')
	projects=Project.objects.filter(Q(user=user.user.id)).order_by('-endyear')
	publications=Publication.objects.filter(Q(user=user.user.id)).order_by('-id')
	students=Student.objects.filter(Q(user=user.user.id)).order_by('-id')
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
			user=Profile.objects.get(user__username=username)
			query=QueryModel()
			query.name=request.POST['name']
			query.email=request.POST['email']
			query.subject=request.POST['subject']
			query.message=request.POST['message']
			query.user=user.user

	        # user=Profile.objects.get(user=request.user)
	        # noti=Notification(user=user,message=subject,text=text,is_read=0)
        	# user.notif = user.notif +1
        	# noti.save()
        	# user.save()

			user=Profile.objects.get(user=request.user)
			noti=Notification(user=user,message=subject,text=text,is_read=0)
			user.notif = user.notif +1
			noti.save()
			user.save()

			query.save()
			suc_message='<i class="fa fa-check"></i>Your message was sent, thank you!'
			return render(request,'teacher.html',{'user':user,'course':course,'incourse':incourse,'education':education,'education':education,'projects':projects,'publications':publications,'suc_message':suc_message,error_message:''})
		elif len(request.POST['name']) > 1:
			error_message = '<i class="fa fa-exclamation-circle"></i> Invalid Captcha.'
			return render(request,'teacher.html',{'user':user,'course':course,'incourse':incourse,'education':education,'education':education,'projects':projects,'publications':publications,'error_message':error_message,'suc_message':""})
	else:
		return render(request,'teacher.html',{'user':user,'course':course,'incourse':incourse,'education':education,'projects':projects,'publications':publications,'students':students,'error_message':"",'suc_message':""})
