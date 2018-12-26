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
from django.views.static import serve
from userpage import views as u_view

urlpatterns = [
    url(r'^$', views.Login.as_view()),
    url(r'^a/logout/', views.Logout.as_view()),
    url(r'^a/activity/', views.ActivityList.as_view()),
    url(r'^a/lottery/', views.LotteryList.as_view()),
    url(r'^a/barrage/', views.SetComment.as_view()),
    url(r'^a/programe/', views.ProgrameList.as_view()),
    url(r'^a/Lottery/create/', views.LotteryCreate.as_view()),
    url(r'^a/Lottery/edit/', views.LotteryDetail.as_view()),
    url(r'^a/Lottery/delete/', views.LotteryDelete.as_view()),
    url(r'^a/Activity/create/', views.ActivityCreate.as_view()),
    url(r'^a/Activity/edit/', views.ActivityDetail.as_view()),
    url(r'^a/Activity/delete/', views.ActivityDelete.as_view()),
    url(r'^a/Barrage/left/', views.barrage_left_detele.as_view()),
    url(r'^a/Barrage/right_detail/', views.barrage_right_detele.as_view()),
    url(r'^a/Programe/delete/', views.ProgrameDelete.as_view()),
    url(r'^a/Programe/up/', views.ProgrameUp.as_view()),
    url(r'^a/Programe/down/', views.ProgrameDown.as_view()),
    url(r'^a/Programe/create/', views.ProgrameCreate.as_view()),
    url(r'^a/Programe/edit/', views.ProgrameDetail.as_view()),
    url(r'^BarrierWall/', views2.BarrierWall.as_view()),
    url(r'^b/Line/', views.Line.as_view()),
    url(r'^b/Top/', views.Top.as_view()),
    url(r'^b/Pic/', views.Pic.as_view()),
    url(r'^b/Barrier/', views.Barrier.as_view()),
    url(r'^m/(?P<path>.*)$', serve, {'document_root': 'static/'}),
    url(r'^api/u/activity/list', u_view.ActivityList.as_view()),
    url(r'^api/u/activity/detail',u_view.ActivityDetail.as_view()),
    url(r'^api/u/activity/program',u_view.ProgramDetail.as_view()),
    url(r'^api/u/lottery/list',u_view.LotteryInfo.as_view()),
    url(r'^api/u/activity/comment',u_view.SetComment.as_view()),
    url(r'^api/u/activity/picture',u_view.SetPicture.as_view()),
]
