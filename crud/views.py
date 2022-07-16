from rest_framework.views import APIView
from rest_framework.generics import (CreateAPIView,GenericAPIView,)
from django.shortcuts import render
from .models import *
from rest_framework.permissions import IsAuthenticated, AllowAny

#Crud Operation By Html,Css and JavaScript(Web)
from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render, redirect  
from crud.forms import EmployeeForm 

class CreateAndGetTaskView(TemplateView):
    def get(self,request,*args,**kwargs):
        emp=TaskTable.objects.all()
        return render(request,'crud_temp/show.html',{'emp':emp})

def CreateData(request):
    if request.method=='POST':
        form = EmployeeForm(data=request.POST or None)
        if form.is_valid():
            try:
                form.save()
                return redirect('GetTaskView')
            except:
                pass
    else:
        form = EmployeeForm()  
    return render(request,'crud_temp/index.html',{'form':form})  

def edit(request,id):
    emp=TaskTable.objects.get(id=id)
    return render(request, 'crud_temp/edit.html',{'emp':emp})

def update(request,id):
    emp=TaskTable.objects.get(id=id)
    form=EmployeeForm(request.POST,instance=emp)
    if form.is_valid():
        form.save()
        return redirect('GetTaskView')
    return render(request, 'crud_temp/edit.html', {'emp': emp}) 

def delete(request,id):
    emp=TaskTable.objects.get(id=id)
    emp.delete()
    return redirect('GetTaskView')