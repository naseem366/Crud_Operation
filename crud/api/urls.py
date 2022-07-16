from django.conf.urls import url
from django.urls import path
from .views import *

urlpatterns = [
    path('post_get',Post_Get.as_view()),
    path('post_get/<int:pk>',Post_Get.as_view()),
    path('CreateUserAPIView',CreateUserAPIView.as_view()),
    path('CreateUserAPIView/<int:pk>',CreateUserAPIView.as_view()),
    path('loginUserAPIView',loginUserAPIView.as_view()),
    path('CreateUserAddressAPIView',CreateUserAddressAPIView.as_view()),
    path('get_single_address',get_single_address.as_view()),
    path('delete_address',delete_address.as_view()),
]
