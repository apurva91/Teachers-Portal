from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import json
import urllib
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from portal.models import Profile
from django.views import generic

def index(request):
	return HttpResponse("Hello")

class IndexView(generic.ListView):
    model = Profile
    template_name = 'index.html'
    context_object_name = 'all_items'

	# def get_queryset(self):
    #     return Profile.objects.all()

def fac_home(request, pk):
	fac = Profile.objects.get(pk=pk)
	context = {'fac' : fac}
	return render(request, 'homepage.html', context)
