"""DjangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from adminpage import views
from barragepage import views as views2

urlpatterns = [

    url(r'^a/login/', views.Login.as_view()),
    url(r'^a/logout/', views.Logout.as_view()),
    #url(r'^a/register/', views.Register.as_view()),
    url(r'^a/activity/', views.ActivityList.as_view()),
    url(r'^a/lottery/', views.LotteryList.as_view()),
    url(r'^a/barrage/', views.SetComment.as_view()),
    url(r'^a/programe/', views.ProgrameList.as_view()),
    url(r'^a/Lottery/create/', views.LotteryCreate.as_view()),
    url(r'^a/Lottery/edit/', views.LotteryDetail.as_view()),
    url(r'^a/Activity/create/', views.ActivityCreate.as_view()),
    url(r'^a/Activity/edit/', views.ActivityDetail.as_view()),
    url(r'^a/Activity/delete/', views.ActivityDelete.as_view()),
    url(r'^a/Barrage/left/', views.barrage_left_detele.as_view()),
    url(r'^a/Barrage/left_create/', views.barrage_left_create.as_view()),
    url(r'^a/Barrage/right_detail/', views.barrage_right_detele.as_view()),
    url(r'^a/Barrage/right_create/', views.barrage_right_create.as_view()),
    url(r'^a/Programe/delete/', views.ProgrameDelete.as_view()),
    url(r'^a/Programe/up/', views.ProgrameUp.as_view()),
    url(r'^a/Programe/down/', views.ProgrameDown.as_view()),
    url(r'^a/Programe/create/', views.ProgrameCreate.as_view()),
    url(r'^a/Programe/edit/', views.ProgrameDetail.as_view()),
    url(r'^b/1/', views2.BarrierWall.as_view()),\
]
