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
from django.conf import Settings
import uuid

class ExportExcle(APIView):
    def post(self,request):
        file_obj=UploadFile.objects.create(file=request.FILES['file'])
        df=pd.read_csv(f"{settings.BASE_DIR}/media_cdn/{file_obj.file}",encoding='ISO-8859-1',header=None, engine='c',lineterminator='\n', sep=';')
        for student in (df.values.tolist()):
            # data={
            # 'student':student[0]
            # }
            print(student)
        return Response({'message':'Image and File has been successfully Upload'},status=HTTP_200_OK)

