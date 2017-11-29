
# Register your models here.
from django.contrib import admin
from .models import Profile, CoursePage, Course, Education, Publication, Student
admin.site.register(Profile)
admin.site.register(CoursePage)
admin.site.register(Course)
admin.site.register(Education)
admin.site.register(Publication)
admin.site.register(Student)
