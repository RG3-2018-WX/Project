# -*- coding: utf-8 -*-
#    
from django.conf.urls import url

from userpage.views import *




urlpatterns = [

    url(r'^activity/list/?$', ActivityList.as_view()),
    url(r'^activity/detail/?$', ActivityDetail.as_view()),
    url(r'^activity/program/?$', ProgramDetail.as_view()),
    url(r'^lottery/list/?$', LotteryInfo.as_view()),
    url(r'^activity/comment/?$', SetComment.as_view()),
    url(r'^activity/picture/?$', SetPicture.as_view()),
    url(r'^activity/user/?$',InsertActivityUser.as_view())
]
