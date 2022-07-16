from django.conf.urls import url
from django.urls import path
from .views import *
from crud import views

urlpatterns = [

#Crud Operation By Html,Css and JavaScript(Web)

    path("GetTaskView",CreateAndGetTaskView.as_view(),name="GetTaskView"),
    path("CreateData",CreateData,name="CreateData"),
    #path("CreateAndTaskView",CreateAndTaskView.as_view(),name="CreateAndTaskView")
    path("edit/<int:id>",edit,name="edit"),
    path("update/<int:id>",update,name="update"),
    path("delete/<int:id>",delete,name="delete"),
    #path("show",show,name="show")
    
    
]
