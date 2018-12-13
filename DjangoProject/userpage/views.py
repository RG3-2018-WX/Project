from django.shortcuts import render
from codex.baseerror import *
from codex.baseview import APIView
from django.utils import timezone
from DjangoProject.models import ActivityUser,Activity,LotteryResult,Comment, Barrage, Picture
import json
import datetime
import re

class ActivityList(APIView):
    def get(self):
        show_list = ActivityUser.activitySelcetedByUser(self.input['openId'])
        list = []
        for activity in show_list:
            list.append(
                {
                    'name': activity.name,
                    'description': activity.description,
                    'startTime':activity.start_time,
                    'place': activity.place,
                    'endTime':activity.end_time
                }
            )
        if list:
            return list
        else:
            raise InputError('the user attend no activity')

class ActivityDetail(APIView):
    def get(self):
        self.check_input('activityId')
        program_list = Programe.selectByActivity(Activity.selectById(self.input['activityId']))
        if not program_list:
            raise InputError('no such activity')
        show_list = []
        for program in program_list:
            show_list.append(
                {
                    'name': program.name,
                    'sequence': program.sequence,
                    'actor': program.actor
                }
            )
        return show_list
class ProgramDetail(APIView):
    def get(self):
        self.check_input('sequence','activityId')
        program = Program.objects.get(activity__id=input(['activityId']),sequence=input(['sequence']))
        if not program:
            raise InputError('no such program')
        show = {
            'name':program.name,
            'description':program.description,
            'actor':program.actor
        }
        return show
class LotteryInfo(APIView):
    def get(self):
        self.check_input('openId','activityId')
        lottery_result = LotteryResult.objects.filter(open_id=self.input['openId'],lottery__activity__id=self.input['activityId'])
        if lottery_result :
            show_list = []
            for i in lottery_result:
                show_list.append({
                    'name': i.lottery.name,
                    'prize':i.prize
                })
        return show_list
class SetComment(APIView):
    def post(self):
        self.check_input('openId')
        Comment.insertComment(Activity.selectById(self.input['activityId']), self.input['openId'],
                              self.input['color'], self.input['content'],
                              self.input['bolt'], self.input['underline'], self.input['incline'], timezone.now(),
                              Barrage.OK)


class SetPicture(APIView):
    def post(self):
        self.check_input('openId')
        Picture.insertComment(Activity.selectById(self.input['activityId']), self.input['openId'], self.input['picUrl'],
                              timezone.now(),
                              Barrage.OK)
