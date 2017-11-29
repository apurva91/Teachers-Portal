from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from django.db.models import Q
import requests, tempfile, os, random, string, json, urllib,re
from django.core import files
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

from oauth2client.client import GoogleCredentials
credentials = GoogleCredentials.get_application_default()

def PWDGen(length):
   letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
   return ''.join(random.choice(letters) for i in range(length))

def PassReset(email):
    client = requests.session()
    client.get('http://localhost:8000/portal/forgot/')
    csrftoken = client.cookies['csrftoken']
    data = dict(email=email,csrfmiddlewaretoken=csrftoken)
    r = client.post('http://localhost:8000/portal/forgot/',data=data)
    return r

def create_new_user(request):
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
            email = request.POST['email']
            username = request.POST['username']
            name = request.POST['name']
            if User.objects.filter(username=username).count() is not 0:
                return render(request, 'registration/newuser.html', {'error_message': 'Username Already Exists'})
            if User.objects.filter(email=email).count() is not 0:
                return render(request, 'registration/newuser.html', {'error_message': 'Email Already Registered'})
            user = User.objects.create_user(username=username,password=PWDGen(32),email=email)
            user.save()
            profile = Profile(user=user,name=name,webmail=email)
            profile.save()
            x = PassReset(email)
            return redirect('/portal/newuser/')
        else:
            return render(request, 'registration/newuser.html', {'error_message': 'Invalid Captcha.'})
    else:
        return render(request, 'registration/newuser.html')


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
    return render(request,'portal/dash.html')

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

def CrawlGet(start,end,code):
    urls=[]
    for item in code.split(end):
        if start in item:
            urls.append(item [item.find(start)+len(start) : ])
    return urls

def Extract_Stud(content,user_id):
    x=""
    user=Profile.objects.get(user=user_id)
    for item in content.split("<!-- END PHD STUDENT ONGOING SECTION -->"):
        if '<!-- START PHD STUDENT ONGOING SECTION -->' in item:
            x+=  item [item.find('<!-- START PHD STUDENT ONGOING SECTION -->')+len('<!-- START PHD STUDENT ONGOING SECTION -->') : ]
    lis=[]  
    pub=[]
    pub = CrawlGet('<li>','</li>',x)
    for item in pub:
        pli=Student(name=item,completed=False,degree=1)
        pli.user=user.user
        user.students = user.students + 1
        pli.save()
    x=""
    for item in content.split("<!-- END MTech STUDENT ONGOING SECTION -->"):
        if '<!-- START MTech STUDENT ONGOING SECTION -->' in item:
            x+=  item [item.find('<!-- START MTech STUDENT ONGOING SECTION -->')+len('<!-- START MTech STUDENT ONGOING SECTION -->') : ]

    pub = CrawlGet('<li>','</li>',x)
    for item in pub:
        pli=Student(name=item,completed=False,degree=2)
        user.students = user.students + 1
        pli.user=user.user
        pli.save()
    x=""
    for item in content.split("<!-- END PHD STUDENT COMPLETED SECTION -->"):
        if '<!-- START PHD STUDENT COMPLETED SECTION -->' in item:
            x+=  item [item.find('<!-- START PHD STUDENT COMPLETED SECTION -->')+len('<!-- START PHD STUDENT COMPLETED SECTION -->') : ]

    pub = CrawlGet('<li>','</li>',x)
    for item in pub:
        pli=Student(name=item,completed=False,degree=1)
        pli.user=user.user
        pli.thesis_title=item.split("</em>")[3].split("&diam;")[0][2:-1]
        pli.name=item.split("</em>")[2].split("&diam;")[0][1:]
        pli.supervisors=item.split("</em>")[1].split("&diam;")[0][1:]
        user.students = user.students + 1
        pli.save()

    x=""
    for item in content.split("<!-- END MTech STUDENT COMPLETED SECTION -->"):
        if '<!-- START MTech STUDENT COMPLETED SECTION -->' in item:
            x+=  item [item.find('<!-- START MTech STUDENT COMPLETED SECTION -->')+len('<!-- START MTech STUDENT COMPLETED SECTION -->') : ]

    pub = CrawlGet('<li>','</li>',x)
    for item in pub:
        pli=Student(name=item,completed=False,degree=2)
        pli.user=user.user
        pli.thesis_title=item.split("</em>")[3].split("&diam;")[0][2:-1]
        pli.name=item.split("</em>")[2].split("&diam;")[0][1:]
        pli.supervisors=item.split("</em>")[1].split("&diam;")[0][1:]
        user.students = user.students + 1
        pli.save()
    user.save()


def Extract_Course(content,user_id):
    x=""
    y=""
    for item in content.split("<!-- END COURSES OFFERED SECTION-->"):
        if '<!-- START COURSES OFFERED SECTION -->' in item:
            x+=  item [item.find('<!-- START COURSES OFFERED SECTION -->')+len('<!-- START COURSES OFFERED SECTION -->') : ]
    lis=[]
    for item in x.split("</li>"):
        if('<li>') in item:
            final = item [item.find('<li>')+len('<li>') : ]
            mylist = re.split(' \xe2\x8b\x84 | &diam; | : |-',final)
            lis.append(mylist)
    user = Profile.objects.get(id=user_id)
    for idx,item in enumerate(lis):
        course = Course()
        course.user=user.user
        course.startdate=item[0].replace(" ","")
        course.enddate=item[1]
        if item[2][0]=="E":
            course.semester=2
        else:
            course.semester=1
        course.course_id=item[3]
        course.title=item[4].replace("&amp;","&")
        course.active=0
        course.url="#"
        user.courses=user.courses+1
        user.save()
        course.save()

def Extract_Profile(content,user_id):
    x=""
    for item in content.split("<!-- END PROFILE INFO SECTION -->"):
        if '<!-- START PROFILE INFO SECTION -->' in item:
            x+=  item [item.find('<!-- START PROFILE INFO SECTION -->')+len('<!-- START PROFILE INFO SECTION -->') : ]
    lis=[]

    for item in x.split("\" alt=\""):
        if '<img src=\"' in item:
            lis.append("iitg.ernet.in"+ item [item.find('<img src=\"')+len('<img src=\"') : ])

    for item in re.split('<br />|</p>',x):
        if ':' in item:
            lis.append(item [item.find(':')+len(':') : ])
    lis.pop()

    for idx,item in enumerate(x.split("</div>")):
        if '<p>' in item:
            if idx==1:
                for idx,item2 in enumerate(item.split("</label>")):
                    if '<label>' in item2:
                        lis.append(item2 [item2.find('<label>')+len('<label>') : ])

                y = (item [item.find('<p>')+len('<p>') : ])
                v = re.split("<br />|,",y)
                lis.append(v[0])
                lis.append(v[1])
    user = Profile.objects.get(id=user_id)
    # if lis[0][0]=='h' and lis[0][1]=='t':
    #     user.avatar=lis[0]
    # else:
    #     user.avatar="http://"+lis[0]
    user.office=lis[1]+", CSE Department, IIT Guwahati"
    user.residence="Qtr No. " + lis[4]+", CSE Department, IIT Guwahati"
    user.webmail=lis[3].replace(" ","")
    user.name=lis[6]
    user.designation=lis[7]
    user.phone=lis[2]
    user.save()

def Extract_Pub(content,user_id):
    x=""
    for item in content.split("<!-- END Publications SECTION -->"):
        if '<!-- START Publications SECTION -->' in item:
            x+=  item [item.find('<!-- START Publications SECTION -->')+len('<!-- START Publications SECTION -->') : ]
    lis=[]  
    pub=[]
    for item in x.split("</p>"):
        if '<p align="justify">' in item:
            pub.append(item [item.find('<p align="justify">')+len('<p align="justify">') : ])
    y=""
    user=Profile.objects.get(user=user_id)
    for idx,item in enumerate(pub):
        pubs = Publication()
        user.publications = user.publications + 1
        pubs.user = user.user
        pubs.authors = item.split('"')[0][:-2]
        pubs.title = item.split('"')[1]
        pubs.journal = item.split(item.split('"')[1])[1][3:]
        pubs.save()
    user.save()

def Extract_Edu(content,user_id):
    x=""
    for item in content.split("<!-- END ACADEMIC PROFILE SECTION -->"):
        if '<!-- START ACADEMIC PROFILE SECTION -->' in item:
            x+=  item [item.find('<!-- START ACADEMIC PROFILE SECTION -->')+len('<!-- START ACADEMIC PROFILE SECTION -->') : ]
    pub=[]
    for item in x.split("</p>"):
        if '<p align="justify">' in item:
            pub.append(item [item.find('<p align="justify">')+len('<p align="justify">') : ])
    user = User.objects.get(id=user_id)
    for item in pub:
        edu = Education()
        edu.user=user
        for item2 in item.split("</strong>"):
            if '<strong>' in item2:
                edu.degree=item2 [item2.find('<strong>')+len('<strong>') : ]
        for item2 in item.split(","):
            if '<br />' in item2:
                x = item2 [item2.find('<br />')+len('<br />') : ].replace("\n","").replace("\t","")
                edu.desc=str(x)[8:]
        edu.institute= item.split(",",1)[-1][1:-7]
        edu.year=int(item.split(",")[-1][1:-1])
        edu.save()

def Extract_Project(content,user_id):
    x=""
    for item in content.split("<!-- END SPONSORED RESEARCH PROJECTS SECTION -->"):
        if '<!-- START SPONSORED RESEARCH PROJECTS SECTION -->' in item:
            x+=  item [item.find('<!-- START SPONSORED RESEARCH PROJECTS SECTION -->')+len('<!-- START SPONSORED RESEARCH PROJECTS SECTION -->') : ]
    lis=[]
    pub=[]
    for item in x.split("</p>"):
        if '<p align="justify">' in item:
            pub.append(item [item.find('<p align="justify">')+len('<p align="justify">') : ])
    y=""
    user = Profile.objects.get(id=user_id)
    for item in pub:
        proj = Project()
        proj.user = user.user
        user.projects = user.projects + 1
        for item2 in CrawlGet('<strong>','<br />', item):
            a =  item2.split('</strong>')[0][:-1]
            b = item2.split('</strong>')[1][1:]
            if a == "Project Title":
                proj.title = b[1:-1]
            elif a == "Co-PI":
                proj.copi=b
            elif a == "PI":
                proj.pi=b
            elif a == "Funding Agency":
                proj.funding=b
            elif a == "Start Year":
                proj.startyear=b
            elif a == "End Year":
                proj.endyear = b
        proj.save()
    user.save()

def Extractor(url,user_id):
    response = urllib.request.urlopen(url)
    content = response.read()
    content=str(content)
    # content = content.encode("utf8")
    Extract_Profile(content,user_id)
    Extract_Course(content,user_id)
    Extract_Edu(content,user_id)
    Extract_Project(content,user_id)
    Extract_Pub(content,user_id)
    Extract_Stud(content,user_id)

def submitLink(request):
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid:
            x = request.POST['link']
            # return HttpResponse(Extractor(x,request.user.id))
            Extractor(x,request.user.id)
            return redirect('/portal/')
    else:
        form = LinkForm()
        return render(request,'portal/submit.html',{'form':form})

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
            tempuser = Profile.objects.get(user=request.user)
            if course.active and not course1.active:
                    tempuser.active_courses = tempuser.active_courses - 1
            elif course1.active and not course.active:
                tempuser.active_courses = tempuser.active_courses + 1
            tempuser.save()
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

def list_all_education(request):
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.user=request.user
            education.save()
            return redirect('/portal/education/')
    else:
        form = EducationForm()
    education = Education.objects.filter(Q(user=request.user)).order_by('-year')
    # incourse = Course.objects.filter(Q(user=request.user) & Q(active=0)).order_by('-enddate')
    return render(request, 'portal/education.html', {'form': form, 'education':education})

def edit_education(request,id):
    if request.method == 'POST':
        form=EducationForm(request.POST)
        if form.is_valid():
            education = Education.objects.get(id=id)
            if education.user.id != request.user.id:
                return HttpResponse('404'+str(request.user)+str(education.user))
            education1=form.save(commit=False)
            education.degree=education1.degree
            education.desc=education1.desc
            education.institute=education1.institute
            education.year=education1.year
            education.save()
            return redirect('/portal/education/')
    return redirect('/portal/education/')

def delete_education(request,id):
    if request.method == 'POST':
        education = Education.objects.get(id=id)
        if education.user != request.user:
            return HttpResponse('Dont Try To Mess With The System')
        # if education.active:
        #     tempuser.active_education = tempuser.active_education -1
        education.delete()

        return redirect('/portal/education/')
    return redirect('/portal/education/')

def list_all_projects(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user=request.user
            tempuser = Profile.objects.get(user=request.user)
            tempuser.projects = tempuser.projects +1
            tempuser.save()
            project.save()
            return redirect('/portal/projects/')
    else:
        form = ProjectForm()
    projects = Project.objects.filter(Q(user=request.user)).order_by('-endyear')
    # incourse = Course.objects.filter(Q(user=request.user) & Q(active=0)).order_by('-enddate')
    return render(request, 'portal/project.html', {'form': form, 'projects':projects})

def edit_project(request,id):
    if request.method == 'POST':
        form=ProjectForm(request.POST)
        if form.is_valid():
            project = Project.objects.get(id=id)
            if project.user.id != request.user.id:
                return HttpResponse('404'+str(request.user)+str(project.user))
            project1=form.save(commit=False)
            project.title=project1.title
            project.pi=project1.pi
            project.copi=project1.copi
            project.funding=project1.funding
            project.startyear=project1.startyear
            project.endyear=project1.endyear
            project.save()
            return redirect('/portal/projects/')
    return redirect('/portal/projects/')

def delete_project(request,id):
    if request.method == 'POST':
        project = Project.objects.get(id=id)
        if project.user != request.user:
            return HttpResponse('Dont Try To Mess With The System')
        # if projects.active:
        #     tempuser.active_projects = tempuser.active_projects -1
        tempuser = Profile.objects.get(user=request.user)
        tempuser.projects = tempuser.projects -1
        tempuser.save()
        project.delete()

        return redirect('/portal/projects/')
    return redirect('/portal/projects/')

def list_all_publications(request):
    if request.method == 'POST':
        form = PublicationForm(request.POST)
        if form.is_valid():
            publication = form.save(commit=False)
            publication.user=request.user
            tempuser = Profile.objects.get(user=request.user)
            tempuser.publications = tempuser.publications +1
            tempuser.save()
            publication.save()
            return redirect('/portal/publications/')
    else:
        form = PublicationForm()
    publications = Publication.objects.filter(Q(user=request.user)).order_by('-id')
    # incourse = Course.objects.filter(Q(user=request.user) & Q(active=0)).order_by('-enddate')
    return render(request, 'portal/publication.html', {'form': form, 'publications':publications})

def edit_publication(request,id):
    if request.method == 'POST':
        form=PublicationForm(request.POST)
        if form.is_valid():
            publication = Publication.objects.get(id=id)
            if publication.user.id != request.user.id:
                return HttpResponse('404'+str(request.user)+str(publication.user))
            publication1=form.save(commit=False)
            publication.title=publication1.title
            publication.authors=publication1.authors
            publication.journal=publication1.journal
            publication.save()
            return redirect('/portal/publications/')
    return redirect('/portal/publications/')

def notivi(request):
    noti=Notification.objects.filter(user=request.user)
    user=Profile.objects.get(user=request.user)
    user.notif=0
    user.save()
    return render(request, 'portal/student.html', {'noti':noti})


def delete_publication(request,id):
    if request.method == 'POST':
        publication = Publication.objects.get(id=id)
        if publication.user != request.user:
            return HttpResponse('Dont Try To Mess With The System')
        # if projects.active:
        #     tempuser.active_projects = tempuser.active_projects -1
        tempuser = Profile.objects.get(user=request.user)
        tempuser.publications = tempuser.publications -1
        tempuser.save()
        publication.delete()

        return redirect('/portal/publications/')
    return redirect('/portal/publications/')

def list_all_students(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.user=request.user
            tempuser = Profile.objects.get(user=request.user)
            tempuser.students = tempuser.students +1
            tempuser.save()
            student.save()
            return redirect('/portal/students/')
    else:
        form = StudentForm()
    students = Student.objects.filter(Q(user=request.user) & Q(completed=0)).order_by('-id')
    paststudents = Student.objects.filter(Q(user=request.user) & Q(completed=1)).order_by('-id')
    # incourse = Course.objects.filter(Q(user=request.user) & Q(active=0)).order_by('-enddate')
    return render(request, 'portal/student.html', {'form': form, 'students':students, 'paststudents':paststudents,})

def edit_student(request,id):
    if request.method == 'POST':
        form=StudentForm(request.POST)
        if form.is_valid():
            student = Student.objects.get(id=id)
            if student.user.id != request.user.id:
                return HttpResponse('404'+str(request.user)+str(student.user))
            student1=form.save(commit=False)
            student.name=student1.name
            student.degree=student1.degree
            student.thesis_title=student1.thesis_title
            student.supervisors=student1.supervisors
            student.completed=student1.completed
            student.save()
            return redirect('/portal/students/')
    return redirect('/portal/students/')

def delete_student(request,id):
    if request.method == 'POST':
        student = Student.objects.get(id=id)
        if student.user != request.user:
            return HttpResponse('Dont Try To Mess With The System')
        # if projects.active:
        #     tempuser.active_projects = tempuser.active_projects -1
        tempuser = Profile.objects.get(user=request.user)
        tempuser.students = tempuser.students -1
        tempuser.save()
        student.delete()

        return redirect('/portal/students/')
    return redirect('/portal/students/')

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

def entities_text(text,sent_score,sent_mag):
    """Detects entities in the text."""
    client = language.LanguageServiceClient()

    # if isinstance(text, six.binary_type):
    #     text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects entities in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    entities = client.analyze_entities(document).entities

    # entity types from enums.Entity.Type
    entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                   'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')
    
    isMeeting=0
    isReview=0
    isDoubt=0
    isPromotion=0

    naam=""
    loc=""
    eve=""
    course=""
    post=""
    output=""
    for entity in entities:
        if entity.name.lower()=='review' or entity.name.lower()=='feedback':
            isReview=1
        if entity.name.lower()=='meeting':
            isMeeting=1
        if entity.name.lower()=='doubt':
            isDoubt=1
        if entity.name.lower()=='promotion':
            isPromotion=1
        if entity.type==1 and entity.salience>0.1:
            naam=entity.name
        if entity.type==4:
            eve=entity.name
        if entity.type==2:
            loc=entity.name
        if entity.type==1 and 0.04<entity.salience<0.06:
            post=entity.name

    if isReview==1:

        if sent_score<0:
            output='You have a Critical Review '
        if sent_score>0:
            output='You have a Positive Review '

    if isMeeting==1:
        if len(loc)>0:
            output="Hey "+naam+",You have a " +eve+" at "+loc + " on 29/11/2017 "
        else:
            output="Hey "+naam+",You have a " +eve+ " on 29/11/2017 "

    if isDoubt==1:
        output='You have 1 new doubt'
    if isPromotion==1 and sent_score>0.35:    
        output='Congratulations,'+naam+' you have been promoted to '+post
     
    return output

def Analyze(text):
    client=language.LanguageServiceClient()

    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT
    )
    sentiment = client.analyze_sentiment(document=document).document_sentiment

    sent_score=sentiment.score
    sent_mag=sentiment.magnitude
    return entities_text(text,sent_score,sent_mag) 

def upload_analyze(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        user=Profile.objects.get(user=request.user)
        Notif = Analyze(myfile.read().decode("utf-8"))
        # noti=Notification(user=user,message=Notif,is_read=0)
        # user.notif = user.notif + 1
        # noti.save()
        # user.save()
        return HttpResponse(Notif)
    return render(request, 'portal/upload.html')

