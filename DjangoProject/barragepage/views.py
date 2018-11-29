from django.shortcuts import render
from codex.baseerror import *
from codex.baseview import APIView
from django.contrib.auth.models import User

from django.contrib.auth import authenticate

from DjangoProject import models
from DjangoProject.models import Activity,Comment,Barrage,Picture
from django.utils import timezone
from wechat.views import CustomWeChatView
import uuid
from WeChatTicket import settings
import os

class CommentLinenumber(APIView):
    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please Login First!")
        self.check_input('linenumber')
        return self.input['linenumber']

class SetTop(APIView):

    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please Login First!")
        self.check_input('activityId')
        old_top = Comment.objects.get(status = Barrage.TOP)
        old_top.status = Barrage.NOT_OK
        old_top.save()
        Comment.insertComment(Activity.selectById(self.input['activityId']),self.request.user.username,self.input['color'],self.input['content'],
            self.input['bolt'], self.input['underline'] ,self.input['incline'],timezone.now(),Barrage.TOP)
    def get(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please Login First!")
        top = Comment.objects.get(activity=Activity.selectById(self.input['activityId'])).get(status=Barrage.TOP)
        top_comment = {
            'content': top.content,
            'color': top.color,
            'bolt': top.bolt,
            'incline': top.incline,
            'underline': top.underline
        }
        return top_comment
        pass
class SetComment(APIView):
    comment_id = 0
    pic_id = 0
    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please Login First!")
        self.check_input('activityId')
        if self.check_input('comment'):
            Comment.insertComment(Activity.selectById(self.input['activityId']), self.input['openId'],
                                  self.input['color'], self.input['content'],
                                  self.input['bolt'], self.input['underline'], self.input['incline'], timezone.now(),
                                  Barrage.OK)
        elif self.check_input('picUrl'):
            Picture.insertComment(Activity.selectById(self.input['activityId']), self.input['openId'],self.input['picUrl'],timezone.now(),
                                  Barrage.OK)
    def get(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please Login First!")
        self.check_input('activityId')
        show_list=[]
        comment_list = Comment.objects.filter(id__gt=SetComment.comment_id)
        for comment in comment_list:
            show_list.append(
                {
                    'content': comment.content,
                    'color': comment.color,
                    'bolt': comment.bolt,
                    'incline': comment.incline,
                    'underline': comment.underline
                }
            )
            SetComment.comment_id=comment.id
        pic_list = Picture.objects.filter(id__gt=SetComment.pic_id)
        for pic in pic_list:
            show_list.append(
                {
                    'picUrl':pic.pic_url
                }
            )
            SetComment.pic_id = pic.id
        return show_list
# Create your views here.
