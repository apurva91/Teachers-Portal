from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import json
import urllib
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

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
	                return HttpResponse("Logged In Successfully.")
	            else:
	                return HttpResponse("Account Disabled.")
	        else:
	        	return render(request, 'registration/login.html', {'error_message': 'Invalid Credentials.'})
        else:
            return render(request, 'registration/login.html', {'error_message': 'Invalid Captcha.'})

    return render(request, 'registration/login.html')

def adminForm(request):
    return render(request, 'portal/user.html')

def update_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    user.profile.bio = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...'
    user.save()



def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'portal/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })