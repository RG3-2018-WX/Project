# -*- coding: utf-8 -*-
#
import re
from django.conf.urls import url
from adminpage.views import *

urlpatterns = [
    url(r'^logout/', views.Logout.as_view()),
    url(r'^activity/', views.ActivityList.as_view()),
    url(r'^lottery/', views.LotteryList.as_view()),
    url(r'^barrage/', views.SetComment.as_view()),
    url(r'^programe/', views.ProgrameList.as_view()),
    url(r'^Lottery/create/', views.LotteryCreate.as_view()),
    url(r'^Lottery/edit/', views.LotteryDetail.as_view()),
    url(r'^Lottery/delete/', views.LotteryDelete.as_view()),
    url(r'^Activity/create/', views.ActivityCreate.as_view()),
    url(r'^Activity/edit/', views.ActivityDetail.as_view()),
    url(r'^Activity/delete/', views.ActivityDelete.as_view()),
    url(r'^Barrage/left/', views.barrage_left_detele.as_view()),
    url(r'^Barrage/right_detail/', views.barrage_right_detele.as_view()),
    url(r'^Programe/delete/', views.ProgrameDelete.as_view()),
    url(r'^Programe/up/', views.ProgrameUp.as_view()),
    url(r'^Programe/down/', views.ProgrameDown.as_view()),
    url(r'^Programe/create/', views.ProgrameCreate.as_view()),
    url(r'^Programe/edit/', views.ProgrameDetail.as_view()),
	url(r'^Line/', views.Line.as_view()),
    url(r'^Top/', views.Top.as_view()),
    url(r'^Pic/', views.Pic.as_view()),
    url(r'^Barrier/', views.Barrier.as_view()),
]
