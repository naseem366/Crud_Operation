#Crud Operation By Html,Css and JavaScript(Web)

from django import forms  
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from crud.models import *  

class EmployeeForm1(forms.ModelForm):
    class Meta:
        model=TaskTable
        fields='__all__'

class EmployeeForm(ModelForm):
    name=forms.CharField(error_messages={'required':'name is required', 'blank':'name is required'},max_length=100)
    subject=forms.CharField(error_messages={'required':'name is required', 'blank':'name is required'},max_length=100)
    branch=forms.CharField(error_messages={'required':'name is required', 'blank':'name is required'},max_length=100)

    class Meta:
        model=TaskTable
        fields='__all__'

    def clean(self):
        super(EmployeeForm, self).clean()

        name = self.cleaned_data.get('name')
        subject = self.cleaned_data.get('subject')

        if TaskTable.objects.filter(name=name).exists():
            #raise ValidationError( _('Invalid value: %(value)s'),code='invalid',params={'value': '42'},)
            raise ValidationError('this Name is Already exists so choose Another Name')
            #self._errors['name'] = self.error_class(['this Name is Already exists so choose Another Name'])

        if TaskTable.objects.filter(subject=subject).exists():
            self._errors['name'] = self.error_class(['this subject is Already exists so choose Another subject'])

      
     # raise ValidationError( _('Invalid value: %(value)s'),code='invalid',params={'value': '42'},)