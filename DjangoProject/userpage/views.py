
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

class UserSign(APIView):
    def post(self):
        self.check_input('openId','activityId')
        print("status before",ActivityUser.selectActivityUser(self.input['openId'],self.input['activityId']).status)
        if ActivityUser.onSign(self.input['openId'],self.input['activityId']):
            print("status after",ActivityUser.selectActivityUser(self.input['openId'],self.input['activityId']).status)
            return {'view':40}
        else:
            raise LogicError("You Have Not Followed.")



class ActivityList(APIView):
    def get(self):
        self.check_input('openId')
        show_list = ActivityUser.activitySelectedByUser(self.input['openId'])
        list = []
        for activity in show_list:
            list.append(
                {
					'activityId':activity.id,
                    'name': activity.name,
                    'description': activity.description,
                    'startTime':activity.start_time,
                    'place': activity.place,
                    'endTime':activity.end_time,
					'sign':activity.sign
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
					'actors': program.actors
				}
			)
		return {'view': 40, 'list': show_list}
		# return show_list


class ProgramDetail(APIView):
	def get(self):
		self.check_input('sequence', 'activityId')
		program = Programe.objects.get(activity__id=input(['activityId']), sequence=self.request.COOKIES['sequence'])
		if not program:
			raise InputError('no such program')
		show = {
			'name': program.name,
			'description': program.description,
			'actors': program.actors
		}
		return {'view': 42, 'show': show, 'sequence': self.request.COOKIES['sequence']}
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
		self.check_input('openId','activityId','color','content','bolt','underline','incline')
		usr = ActivityUser.selectActivityUser(self.input['openId'],self.input['activityId'])
		if usr is None:
			raise LogicError("Not Joined yet!")
		#if usr.status != ActivityUser.SIGN:
		#	raise LogicError("Not Signed yet!")
		Comment.insertComment(activity = Activity.selectById(self.input['activityId']), open_id = self.input['openId'],
		                      color = self.input['color'], content = self.input['content'],
		                      bolt = self.input['bolt'], underline = self.input['underline'], incline = self.input['incline'],time = timezone.now(),
							  status = Barrage.OK)
		return {'view': 40}

class SetPicture(APIView):
	def post(self):
		self.check_input('openId')
		Picture.insertComment(Activity.selectById(self.input['activityId']), self.input['openId'], self.input['picUrl'],
		                      timezone.now(),
		                      Barrage.OK)
		return []

class InsertActivityUser(APIView):
	def post(self):
		self.check_input('openId', 'activityId')
		openid = self.input['openId']
		actid = self.input['activityId']
		activityId = Activity.selectById(actid)
		if activityId is not None:
			ActivityUser.insertActivityUser(openid, activityId)
		else:
			raise InputError('the user attend no activity')
