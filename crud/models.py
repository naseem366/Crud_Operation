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



class File(models.Model):
    name1=models.CharField(max_length=50,blank=True,null=True)
    name2=models.CharField(max_length=50,blank=True,null=True)
    name3=models.CharField(max_length=50,blank=True,null=True)
    created_on=models.DateTimeField(auto_now_add=True)
    

class StudentDetail(models.Model):
    first_name=models.CharField(max_length=50,blank=True,null=True)
    last_name=models.CharField(max_length=50,blank=True,null=True)
    gender=models.CharField(max_length=50,blank=True,null=True)
    country=models.CharField(max_length=50,blank=True,null=True)
    age=models.CharField(max_length=50,blank=True,null=True)
    student_id=models.CharField(max_length=50,blank=True,null=True)
    created_on=models.DateTimeField(auto_now_add=True)


class UploadFile(models.Model):
    file=models.FileField(upload_to='file')

    def __str__(self):
        return str(self.file)