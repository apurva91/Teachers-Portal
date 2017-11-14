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
    avatar = models.ImageField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    designation = models.CharField(max_length=500, blank=True)
    office = models.CharField(max_length=500, blank=True)
    residence = models.CharField(max_length=500, blank=True)
    education = models.CharField(max_length=500, blank=True)
    workexp = models.CharField(max_length=500, blank=True)
    research = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

class Course(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    course_id=models.CharField(max_length=7)
    title=models.CharField(max_length=50)
    year=models.CharField(max_length=10)

class CoursePage(models.Model):
    course=models.ForeignKey(Course, on_delete=models.CASCADE)
    content=RichTextUploadingField()
    #content=HTMLField()

class CourseSubPage(models.Model):
    subpage=models.ForeignKey(CoursePage, on_delete=models.CASCADE)
    #content=HTMLField()
