from django.shortcuts import render
from requests import request
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.status import *
from django.conf import settings
from random import randint
import logging
logger = logging.getLogger('accounts')

# Create your views here.

def check_blank_or_null(data):
	status=True
	for x in data:
		if x=="" or x==None:
			status=False
			break
		else:
			pass					
	return status

class Post_Get(APIView):
    def post(self,request):
        logger.debug('user registration api called')
        logger.debug(request.data)

        serializer=TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Data has been successfully Created'},status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def get(self,request):
        addr=TaskTable.objects.all()
        serializer=ListTaskSerializer(addr,many=True)
        return Response({'data':serializer.data},status=HTTP_200_OK)
    

    def put(self,request,*args,**kwargs):
        pk=self.kwargs.get('pk')
        obj=TaskTable.objects.get(id=pk)
        print("******************",obj)
        serializer=TaskSerializer(data=request.data,instance=obj)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'message':'Data updated Successfully'},status=HTTP_200_OK)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)

    def delete(self,request,*args,**kwargs):
        try:
            TaskTable.objects.get(id=self.kwargs.get('pk')).delete()
            return Response({'message':'Deleted Successfully'},status=HTTP_200_OK)
        except:
            return Response({'message':'Invalid'},status=HTTP_400_BAD_REQUEST)

class CreateUserAPIView(APIView):
    def post(self,request):
        serializer=CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'User has been successfully Created'},status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def get(self,request):
        addr=User.objects.all()
        serializer=ListUserSerializer(addr,many=True)
        return Response({'data':serializer.data},status=HTTP_200_OK)

    def put(self,request,*args,**kwargs):
        pk=self.kwargs.get('pk')
        obj=User.objects.get(id=pk)
        print("******************",obj)
        serializer=CreateUserSerializer(data=request.data,instance=obj)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'message':'Data updated Successfully'},status=HTTP_200_OK)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)

    def delete(self,request,*args,**kwargs):
        try:
            User.objects.get(id=self.kwargs.get('pk')).delete()
            return Response({'message':'Deleted Successfully'},status=HTTP_200_OK)
        except:
            return Response({'message':'Invalid'},status=HTTP_400_BAD_REQUEST)

class loginUserAPIView(APIView):
	permission_classes = (AllowAny,)
	def post(self,request):
		username = request.data.get('username')
		password = request.data.get('password')
		if username is None or password is None:
			return Response({'error': 'Please provide both username and password'},status=HTTP_400_BAD_REQUEST)
		user = authenticate(username=username, password=password)
		if not user:
			returnMessage = {'error': 'Invalid Credentials'}
			return Response(returnMessage,content_type = 'application/javascript; charset=utf8',status=HTTP_400_BAD_REQUEST)
		token, _ = Token.objects.get_or_create(user=user)
		token.save()
		return Response({'token':token.key,'message':"User Login Successfully "},status=HTTP_200_OK)
		

class CreateUserAddressAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        serializer=AddressUserSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'User Adrress has been successfully Created'},status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def get(self,request):
        addr=UserAddress.objects.filter(user=request.user,verify_mobile=True,verify_email=True)
        serializer=ListUserAddressSerializer(addr,many=True)
        return Response({'data':serializer.data},status=HTTP_200_OK)


class get_single_address(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        pk=request.POST['pk']
        if check_blank_or_null([pk]) and UserAddress.objects.filter(user=request.user,pk=pk,verify_mobile=True,verify_email=True).exists():
            addr=UserAddress.objects.get(user=request.user,pk=pk)
            serializer=ListUserAddressSerializer(addr,many=False)
            return Response({'data':serializer.data},status=HTTP_200_OK)
        return Response({'message':"Address Is not exists"}, status=HTTP_400_BAD_REQUEST)
    

class delete_address(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        pk=request.POST['pk']
        if check_blank_or_null([pk]) and UserAddress.objects.filter(user=request.user,pk=pk).exists():
            addr=UserAddress.objects.get(user=request.user,pk=pk)
            addr.delete()
            return Response({'data':"Address successfully delete"},status=HTTP_200_OK)
        return Response({'message':"Address Is not exists"}, status=HTTP_400_BAD_REQUEST)


import pandas as pd
from django.conf import settings
import uuid
import json
from collections import namedtuple
import random

class ExportExcle(APIView):
    def get(self,request):
        student=StudentDetail.objects.all()
        serializer=StudentSerializer(student,many=True)
        df=pd.DataFrame(serializer.data)
        print(df)
        df.to_excel(f"{settings.BASE_DIR}/media_cdn/file/{uuid.uuid4()}.xls",encoding="UTF-8",index=False)
        return Response({'message':'Get Data successfully'},status=HTTP_200_OK)

# [1, 'mohd', 'naseem', 'male', 'india', 25, 1234, '2022-07-30T13:25:16.252122+05:30']
# [3, 'mohd', 'samim', 'male', 'india', 23, 12345, '2022-07-30T17:46:42.730053+05:30']
# [4, 'abdul', 'bari', 'male', 'india', 40, 2342, '2022-07-30T17:47:27.511290+05:30']

    def post(self,request):
        file_obj=UploadFile.objects.create(file=request.FILES['file'])
        df=pd.read_excel(f"{settings.BASE_DIR}/media_cdn/{file_obj.file}")

        student=(df['First Name'].tolist())
        print(student)
        s1 = json.dumps(student)
        x = json.loads(s1, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        lower="abcdefghijklmnopqrstuvwxyz"
        upper="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        number="0123456789"
        symbols="[]{}()*;/,_-"
        all=str(lower) + str(upper) + str(number) + str(symbols)
        length=20
        password="".join(random.sample(all,length))
        password1="".join(random.sample(all,length))
        password2="".join(random.sample(all,length))
        data={
            'name1':x[0],
            'password on first_name':password,
            'name2':x[1],
            'password on secound_name':password1,
            'name3':x[2],
            'password on third_name':password2,

        }
        return Response({'message':'File has been successfully Upload','data':data},status=HTTP_200_OK)

