"""attendence URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL tdo urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
# Padmavathi padma@123
# Mamatha mamat@123
# Deeksha deeks@123
# Avinash avina@123
# Basavaraj basav@123
# Sreeram sreer@123
# Principal princi@123
# HOD hodhod@123

urlpatterns = [
    path("", views.index,name = "index"),
    path("signin",views.handlelogin,name = "signin"),
    path("logout",views.handlelogout,name = "logout"),
    path("login",views.loginpage,name = "loginpage"),
    path("load",views.load,name = "load"),
    path("reqmes",views.reqmes,name = "reqmes"),
    path("attendence",views.attendence,name = "attendence"),
    path("datatopage",views.datatopage,name="datatopage"),
    path("updateattendence",views.updateattendence,name="updateattendence"),
    path("messsages",views.messsages,name = "messsages"),
    path("taskmessages",views.taskmessages,name = "taskmessages"),
    path("tasks",views.tasks,name="tasks"),
    path("accept",views.accept,name= "accept"),
    path("notification",views.notification,name="notification"),
    path("search",views.search,name="search"),
    path("submitresults",views.submitresults,name = "submitresults")
    
]
