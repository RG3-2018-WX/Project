from django.shortcuts import render
from codex.baseerror import *
from codex.baseview import APIView
from django.utils import timezone
from wechat.models import User,Activity,Program,LotteryResult
import json
import datetime
import re

class ActivityList(APIView):
 def get(self):
        show_list = ActivityUser.activitySelcetedByUser(self.input['open_id'])
        list = []
        for i in show_list:
            list.append(
                {
                    'name': i.name,
                    'description': i.description,
                    'startTime':i.start_time,
                    'place': i.place,
                    'endTime':i.end_time
                }
            )
        return list
class ActivityDetail(APIView):
    def get(self):
        self.check_input('activityId')
        program_list = Programe.selectByActivity(Activity.selectById(self.input['activityId']))
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
        show = {
            'name':program.name,
            'description':program.description,
            'actor':program.actor
        }
        return show
class LotteryInfo(APIView):
    def get(self):
        self.check_input('openId','lotteryId')
        lottery_result = LotteryResult.objects.get(open_id=self.input['openId'],lottery__id=self.input['lotteryId'])
        if lottery_result :
            info = lottery_result.prize
            return info
        else:
            raise ValidateError('thank you for attendence')



# Create your views here.
