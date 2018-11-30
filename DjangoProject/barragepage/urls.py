# -*- coding: utf-8 -*-
#
from django.conf.urls import url

from barragepage.views import *




urlpatterns = [
    url(r'^comment/top/?$', SetTop.as_view()),
    url(r'^comment/comment/?$', SetComment.as_view()),
    url(r'^comment/picture/?$', SetPicture.as_view()),
    url(r'^comment/linenumber/?$', CommentLinenumber.as_view())
]
