from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import json
import urllib
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

def index(request):
	return HttpResponse("Hello")