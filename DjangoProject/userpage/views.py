import datetime
import json
import re
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from DjangoProject.models import ActivityUser, Activity, LotteryResult, Comment, Barrage, Picture, Programe
from codex.baseerror import *
from codex.baseview import APIView

class ActivityList(APIView):
    def get(self):
        show_list = Activity.objects.all()
        list = []
        for activity in show_list:
            list.append(
                {
					'activityId':activity.id,
                    'name': activity.name,
                    'description': activity.description,
                    'startTime':activity.start_time,
                    'place': activity.place,
                    'endTime':activity.end_time
                }
            )
        if list:
            return {'view': 40, 'list': list}
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
					'actor': program.actors
				}
			)
		return {'view': 40, 'list': show_list}
		# return show_list


class ProgramDetail(APIView):
	def get(self):
		self.check_input('sequence', 'activityId')
		program = Programe.objects.get(activity__id=input(['activityId']), sequence=input(['sequence']))
		if not program:
			raise InputError('no such program')
		show = {
			'name': program.name,
			'description': program.description,
			'actor': program.actors
		}
		return {'view': 41, 'show': show}
		# return show


class LotteryInfo(APIView):
	def get(self):
		self.check_input('openId', 'activityId')
		lottery_result = LotteryResult.objects.filter(open_id=self.input['openId'],
		                                              lottery__activity__id=self.input['activityId'])
		show_list = []
		if lottery_result:
			for i in lottery_result:
				show_list.append({
					'name': i.lottery.name,
					'prize': i.prize
				})
		return {'view': 40, 'list': show_list}
		# return show_list


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


class ActivityUser(APIView):
	def post(self):
		self.check_input('openId', 'activityId')
		open_id = self.input['openId']
		act_id = self.input['activityId']
		actvity = Activity.selectById(act_id)
		ActivityUser.insertActivityUser(open_id, activity)
