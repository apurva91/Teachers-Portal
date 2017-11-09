from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import OneToOneField


class Profile(models.Model):
    full_name=models.CharField(max_length=30)
    birth_date=models.DateField()
    user = OneToOneField(User,on_delete=models.CASCADE)
