# -*- coding: utf-8 -*-
#

from django.conf.urls import url
from adminpage.views import *





urlpatterns = [
    url(r'^login/?$', Login.as_view()),
    url(r'^logout/?$', Logout.as_view()),
    url(r'^register/?$',Register.as_view()),
    url(r'^activity/status/?$', ActivityStatus.as_view()),
    url(r'^activity/create/?$', ActivityCreate.as_view()),
    url(r'^activity/detail/?$', ActivityDetail.as_view()),
    url(r'^activity/list/?$', ActivityList.as_view()),
    url(r'^lottery/create/?$', LotteryCreate.as_view()),
    url(r'^lottery/detail/?$', LotteryDetail.as_view()),
    url(r'^lottery/delete/?$', LotteryDelete.as_view()),
    url(r'^lottery/status/?$', LotteryStatus.as_view()),
    url(r'^lottery/list/?$', LotteryList.as_view()),
    url(r'^program/delete/?$', ProgrameDelete.as_view()),
    url(r'^program/create/?$', ProgrameCreate.as_view()),
    url(r'^program/detail/?$', ProgrameDetail.as_view()),
    url(r'^program/list/?$', ProgrameList.as_view()),
    url(r'^image/upload/?$', ImageUpload.as_view()),
    url(r'^comment/linenumber/?$', SetCommentLinenumber.as_view()),
    url(r'^comment/comment/?$', SetComment.as_view),
    url(r'^comment/top/?$', SetTop.as_view()),
    url(r'^comment/picture/?$', SetPicture.as_view()),
    url(r'^comment/status/?$',CommentStatus.as_view()),
]
