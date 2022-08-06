from rest_framework.views import APIView
from rest_framework.generics import (CreateAPIView,GenericAPIView,)
from django.shortcuts import render
from .models import *
from rest_framework.permissions import IsAuthenticated, AllowAny
#Crud Operation By Html,Css and JavaScript(Web)
from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render, redirect  
from crud.forms import EmployeeForm,EmployeeForm1

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
    form=EmployeeForm1(request.POST,instance=emp)
    if form.is_valid():
        form.save()
        return redirect('GetTaskView')
    return render(request, 'crud_temp/edit.html', {'emp': emp}) 

def delete(request,id):
    emp=TaskTable.objects.get(id=id)
    emp.delete()
    return redirect('GetTaskView')

from django.http import HttpResponse
from io import BytesIO
import datetime
import xhtml2pdf.pisa as pisa
from xhtml2pdf import pisa
from django.template.loader import get_template


def index(request):
    students=StudentDetail.objects.all()
    return render(request,'crud_temp/pdf.html',{'students':students})

def render_pdf_view(request):
    task_obj=StudentDetail.objects.all()
    print(task_obj)
    template_path = "crud_temp/pdf.html"
    context = {'task_obj': task_obj}
    print(context,"helololololo")

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="task_obj.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)

    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response