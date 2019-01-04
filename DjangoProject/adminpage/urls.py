# -*- coding: utf-8 -*-
#
import re
from django.conf.urls import url
from adminpage.views import *

urlpatterns = [
   url(r'^logout/', Logout.as_view()),
    url(r'^activity/', ActivityList.as_view()),
    url(r'^lottery/', LotteryList.as_view()),
    url(r'^barrage/', SetComment.as_view()),
    url(r'^programe/', ProgrameList.as_view()),
    url(r'^Lottery/create/', LotteryCreate.as_view()),
    url(r'^Lottery/edit/', LotteryDetail.as_view()),
    url(r'^Lottery/delete/', LotteryDelete.as_view()),
    url(r'^Activity/create/', ActivityCreate.as_view()),
    url(r'^Activity/edit/', ActivityDetail.as_view()),
    url(r'^Activity/delete/', ActivityDelete.as_view()),
    url(r'^Barrage/left/', barrage_left_detele.as_view()),
    url(r'^Barrage/right_detail/', barrage_right_detele.as_view()),
    url(r'^Programe/delete/', ProgrameDelete.as_view()),
    url(r'^Programe/up/', ProgrameUp.as_view()),
    url(r'^Programe/down/', ProgrameDown.as_view()),
    url(r'^Programe/create/', ProgrameCreate.as_view()),
    url(r'^Programe/edit/', ProgrameDetail.as_view()),
    url(r'^Line/', Line.as_view()),
    url(r'^Top/', Top.as_view()),
    url(r'^Pic/', Pic.as_view()),
    url(r'^Barrier/', Barrier.as_view()),
]
