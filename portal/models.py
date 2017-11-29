from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
from django.db.models import OneToOneField

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(blank=True,default="1.jpg")
    birth_date = models.DateField(null=True, blank=True)
    designation = models.CharField(max_length=500, blank=True)
    office = models.CharField(max_length=500, blank=True)
    phone=models.CharField(max_length=20,blank=True)
    webmail=models.CharField(max_length=50,blank=True)
    residence = models.CharField(max_length=500, blank=True)
    research = models.CharField(max_length=500, blank=True)
    courses=models.IntegerField(default=0)
    active_courses=models.IntegerField(default=0)
    projects=models.IntegerField(default=0)
    publications=models.IntegerField(default=0)
    students=models.IntegerField(default=0)
    notif=models.IntegerField(default=0)
    def __str__(self):
        return self.user.username

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

class Education(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    degree=models.CharField(max_length=30)
    desc=models.CharField(max_length=200)
    institute=models.CharField(max_length=200)
    year=models.IntegerField()
    def __str__(self):
        return self.degree

ODD_EVEN = (
    (1, ("Odd")),
    (2, ("Even"))
)

class Course(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    course_id=models.CharField(max_length=7)
    title=models.CharField(max_length=50)
    startdate=models.CharField(max_length=4,blank=True)
    enddate=models.CharField(max_length=4,blank=True)
    semester = models.IntegerField(choices=ODD_EVEN, default=1)
    url=models.URLField(blank=True)
    active=models.BooleanField(default=True)

    def __str__(self):
        return self.title

class CoursePage(models.Model):
    course=models.ForeignKey(Course, on_delete=models.CASCADE)
    content=models.TextField()
    #content=HTMLField()

class CourseSubPage(models.Model):
    subpage=models.ForeignKey(CoursePage, on_delete=models.CASCADE)
    #content=HTMLField()

class Project(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=100,blank=True)
    pi=models.CharField(max_length=50,blank=True)
    copi=models.CharField(max_length=100,blank=True)
    funding=models.CharField(max_length=50,blank=True)
    startyear=models.CharField(max_length=10,blank=True)
    endyear=models.CharField(max_length=10,blank=True)

    def __str__(self):
        return self.title

class Publication(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    authors=models.CharField(max_length=50,blank=True)
    title=models.CharField(max_length=100,blank=True)
    journal=models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.title

DEGREE = (
    (1, ("Ph.D.")),
    (2, ("M.Tech.")),
    (3, ("B.Tech."))
)

class Student(models.Model):
        user=models.ForeignKey(User, on_delete=models.CASCADE)
        name=models.CharField(max_length=50)
        degree=models.IntegerField(choices=DEGREE, default=1)
        thesis_title=models.CharField(max_length=100,blank=True)
        supervisors=models.CharField(max_length=80,blank=True)
        completed=models.BooleanField(default=True,blank=True)
        def __str__(self):
            return self.name

class QueryModel(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    message=models.CharField(max_length=500)
    subject=models.CharField(max_length=50)
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)

class Notification(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    message=models.CharField(max_length=250)
    is_read=models.BooleanField(default=0)
    text=models.CharField(max_length=300, blank=True)