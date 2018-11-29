from django.conf.urls import url
from adminpage.views import *





urlpatterns = [
    url(r'^comment/top/?$', SetTop.as_view()),
    url(r'^comment/now/?$', SetComment.as_view()),
    url(r'^comment/linenumber/?$', CommentLinenumber.as_view())
]
    
