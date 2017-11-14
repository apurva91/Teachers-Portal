
# Register your models here.
from django.contrib import admin
from .models import Profile, CoursePage, Course
admin.site.register(Profile)
admin.site.register(CoursePage)
admin.site.register(Course)