from unicodedata import name
from rest_framework.serializers import ModelSerializer, FloatField,Serializer, CharField, ImageField, SerializerMethodField,EmailField,DateField
from crud.models import *
from rest_framework.exceptions import APIException
class APIException400(APIException):
    status_code = 400
class APIException401(APIException):
    status_code = 401

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.conf import settings
from authy.api import AuthyApiClient
authy_api=AuthyApiClient('authy_api')

class TaskSerializer(Serializer):
    name = CharField(error_messages={'required':'name is required', 'blank':'name is required'},max_length=100)
    subject = CharField(error_messages={'required':'subject name is required', 'blank':'subject name is required'},max_length=100)
    branch = CharField(error_messages={'required':'branch is required', 'blank':'branch is required'},max_length=100)

    def validate(self,data):
        name=data.get("name")
        if TaskTable.objects.filter(name=name).exists():
            raise ValidationError("Name is already exists with this Name")
        return data

    def create(self,validated_data):
        name=validated_data.get("name")
        subject=validated_data.get("subject")
        branch=validated_data.get("branch")
        task=TaskTable.objects.create(name=name,subject=subject,branch=branch)
        task.save()

        return validated_data

    def update(self,instance,validated_data):
        name=validated_data.get("name")
        subject=validated_data.get("subject")
        branch=validated_data.get("branch")
        instance.name=name
        instance.subject=subject
        instance.branch=branch
        instance.save()
        return instance

class ListTaskSerializer(ModelSerializer):
    class Meta:
        model=TaskTable
        fields='__all__'


class CreateUserSerializer(Serializer):
    first_name = CharField(error_messages={'required':'first_name is required', 'blank':'first_name is required'},max_length=20)
    last_name = CharField(error_messages={'required':'last_name name is required', 'blank':'last_name name is required'},max_length=20)
    username = CharField(error_messages={'required':'username is required', 'blank':'username is required'},max_length=20)
    email = CharField(error_messages={'required':'email is required', 'blank':'email is required'},max_length=40)
    password = CharField(error_messages={'required':'password name is required', 'blank':'password name is required'},max_length=20)
   
    def validate(self,data):
        username=data.get("username")
        email=data.get("email")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username is already exists with this Username")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email is already exists with this Email")
        return data

    def create(self,validated_data):
        first_name=validated_data.get("first_name")
        last_name=validated_data.get("last_name")
        username=validated_data.get("username")
        email=validated_data.get("email")
        password=validated_data.get("password")
        user=User.objects.create(first_name=first_name,last_name=last_name,username=username,email=email)
        user.set_password(password)
        user.save()
        return validated_data

    def update(self,instance,validated_data):
        first_name=validated_data.get("first_name")
        last_name=validated_data.get("last_name")
        username=validated_data.get("username")
        email=validated_data.get("email")
        password=validated_data.get("password")
        instance.first_name=first_name
        instance.last_name=last_name
        instance.username=username
        instance.email=email
        instance.set_password(password)
        instance.save()

        return validated_data

class ListUserSerializer(ModelSerializer):
    class Meta:
        model=User
        fields='__all__'


class AddressUserSerializer(Serializer):
    city = CharField(error_messages={'required':'city is required', 'blank':'city is required'},max_length=100)
    state = CharField(error_messages={'required':'state name is required', 'blank':'state name is required'},max_length=100)
    country = CharField(error_messages={'required':'country is required', 'blank':'country is required'},max_length=100)
    country_code = CharField(error_messages={'required':'country code is required', 'blank':'country code is required'},max_length=100)
    mobile = CharField(error_messages={'required':'mobile is required', 'blank':'mobile is required'},max_length=100)
    email = CharField(error_messages={'required':'email is required', 'blank':'email is required'},max_length=100)

    def create(self,validated_data):
        user=self.context['request'].user
        city=validated_data.get("city")
        state=validated_data.get("state")
        country=validated_data.get("country")
        mobile=validated_data.get("mobile")
        country_code=validated_data.get('country_code')
        email=validated_data.get("email")
        task=UserAddress.objects.create(user=user,city=city,state=state,country=country,mobile=mobile,email=email,country_code=country_code)
        task.verify_mobile=False
        task.verify_email=False
        task.save()
        return validated_data

class ListUserAddressSerializer(ModelSerializer):
    class Meta:
        model=UserAddress
        fields='__all__'


class StudentSerializer(ModelSerializer):
    class Meta:
        model=StudentDetail
        fields='__all__'