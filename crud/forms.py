#Crud Operation By Html,Css and JavaScript(Web)

from django import forms  
from crud.models import *  
class EmployeeForm(forms.ModelForm): 
    class Meta:  
        model = TaskTable
        fields = "__all__"  
