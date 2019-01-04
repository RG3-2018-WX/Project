from django.shortcuts import render
from codex.baseerror import *
from codex.baseview import APIView
from django.contrib.auth.models import User

from django.contrib.auth import authenticate
from django.http import JsonResponse

from DjangoProject import models
from DjangoProject.models import Activity, Lottery, Programe, Barrage, Comment, Picture
from django.utils import timezone
from django.utils.timezone import now, timedelta
from wechat.views import CustomWeChatView
import uuid
#from WeChatTicket import settings
import os


class BarrierWall(APIView):
    def get(self):
        activity = self.request.COOKIES['activityId']
        result = Activity.selectById(activity)
        r = result.bg_pic_url.name[2:]
        return {'view': 30, 'r': r}


class CommentLinenumber(APIView):
    def get(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please Login First!")
        self.check_input('linenumber')
        return self.input['linenumber']


class SetTop(APIView):
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


class SetComment(APIView):
    def post(self):
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
        self.check_input('activityId', 'commentId')
        show_list=[]
        comment_list = Comment.objects.filter(time__lt=timezone.now().time()+timedelta(seconds=-3)).filter(id__gt=self.input['commentId'])
        for comment in comment_list:
            show_list.append(
                {
                    'id': comment.id,
                    'content': comment.content,
                    'color': comment.color,
                    'bolt': comment.bolt,
                    'incline': comment.incline,
                    'underline': comment.underline
                }
            )
        return show_list
    
    
class SetPicture(APIView):
    def get(self):
        self.check_input('activityId', 'pictureId')
        show_list = []
        pic_list = Comment.objects.filter(time__lt=timezone.now().time.second - 3).filter(id__gt=self.input['pictureId'])
        for pic in pic_list:
            show_list.append(
                {
                    'id': pic.id,
                    'picUrl': pic.pic_url
                }
            )

        return show_list
    
    
# Create your views here.