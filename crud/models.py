from operator import mod
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserAddress(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    city=models.CharField(max_length=20,blank=True,null=True)
    state=models.CharField(max_length=20,blank=True,null=True)
    country=models.CharField(max_length=20,blank=True,null=True)
    

    def __str__(self):
        return str(self.user.email)

        
class TaskTable(models.Model):
    name=models.CharField(max_length=100,blank=True,null=True)
    subject=models.CharField(max_length=100,blank=True,null=True)
    branch=models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return str(self.name)


