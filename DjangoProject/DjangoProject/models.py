from django.db import models
import random, string
from django.contrib.auth.models import User
import django.utils.timezone as timezone
import os
import pandas as pd
import logging


class Activity(models.Model):
	id = models.AutoField(primary_key=True)
	
	def getPath(self):
		return os.path.join('images', self.id)
	
	name = models.CharField(max_length=100)
	place = models.CharField(max_length=100)
	organizer = models.ForeignKey(User, on_delete=models.CASCADE)
	description = models.CharField(max_length=300)
	pic_url = models.ImageField(max_length=255)
	start_time = models.DateTimeField(default=timezone.now)
	end_time = models.DateTimeField(default=timezone.now)
	bg_pic_url = models.ImageField(max_length=255)
	status = models.IntegerField()
	sign = models.IntegerField()
	PREPARING = 0
	RUNNING = 1
	FINISH = 2
	DELETE = 3
	
	@staticmethod
	def insertActivity(organizer, description, pic_url, start_time, end_time, bg_pic_url, status, place, name):
		activity = Activity(organizer=organizer, description=description, pic_url=pic_url, start_time=start_time,
		                    end_time=end_time, bg_pic_url=bg_pic_url, status=status, place=place, name=name)
		activity.sign = random.randint(1000, 9999)
		activity.save()
	
	@staticmethod
	def deleteActivity(id):
		activity = Activity.objects.get(id=id)
		activity.status = Activity.DELETE
		activity.save()
		return True
	
	@staticmethod
	def selectByOrganizer(organizer):
		activities = Activity.objects.filter(organizer=organizer).order_by('start_time')
		return activities
	
	@staticmethod
	def selectById(id):
		try:
			activity = Activity.objects.get(id=id)
		except Exception as e:
			logging.error(e)
			return None
		return activity
	
	@staticmethod
	def updateActivity(id, organizer, description, pic_url, start_time, end_time, bg_pic_url, status, place, name):
		activity = Activity.selectById(id)
		if activity is None:
			return False
		activity.organizer = organizer
		activity.description = description
		activity.pic_url = pic_url
		activity.start_time = start_time
		activity.end_time = end_time
		activity.bg_pic_url = bg_pic_url
		activity.status = status
		activity.place = place
		activity.name = name
		activity.save()
		
		return True


class Programe(models.Model):
	id = models.AutoField(primary_key=True)
	activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
	name = models.CharField(max_length=50, default='')
	description = models.CharField(max_length=300, default='')
	sequence = models.IntegerField()
	actors = models.CharField(max_length=100, default='')
	
	@staticmethod
	def insertPrograme(activity, name, description, sequence, actors):
		programe = Programe(activity=activity, name=name, description=description, sequence=sequence, actors=actors)
		programe.save()
	
	@staticmethod
	def selectById(id):
		try:
			pro = Programe.objects.get(id)
		except Exception as e:
			logging.error(e)
			return None
		return pro
	
	@staticmethod
	def selectByActivity(activity):
		pros = Programe.objects.filter(activity=activity).order_by('sequence')
		return pros
	
	@staticmethod
	def reorderPrograme(activity):
		'''
		将排序好的节目赋予新的sequence，确保正确性
		:param activity:
		:return:
		'''
		pros = Programe.selectByActivity(activity)
		for i in range(len(pros)):
			pros[i].sequence = i
	
	@staticmethod
	def deletePrograme(id):
		programe = Programe.selectById(id)
		if programe is None:
			return False
		else:
			programe.delete()
	
	@staticmethod
	def updatePrograme(id, name='', description='', actors='', sequence=-1):
		pro = Programe.selectById(id)
		if pro is None:
			return False
		if name != '':
			pro.name = name
		if description != '':
			pro.description = description
		if sequence != -1:
			pro.sequence = sequence
		pro.actors = actors
		return True


class ActivityUser(models.Model):
	open_id = models.CharField(max_length=100)
	activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
	status = models.IntegerField()  # 禁言状态,关注状态，签到状态
	NO_SPEAKING = 1
	FOLLOW = 2
	SIGN = 3
	
	def __init__(self):
		self.status = self.FOLLOW
	
	@staticmethod
	def insertActivityUser(open_id, activity):
		if activity is None:
			return False
		t = ActivityUser.objects.filter(activity=activity, open_id=open_id)
		if len(t):
			return False
		actuser = ActivityUser(open_id=open_id, activity=activity)
		actuser.save()
		return True
	
	def onSign(self):
		if self.status != self.NO_SPEAKING:
			self.status = self.SIGN
			return True
		else:
			return False
	@staticmethod
	def activitySelcetedByUser(open_id):
		list = ActivityUser.objects.filter(open_id=open_id)
		showlist = []
		for i in list:
			show_list.append(
				{
					'name': i.activity.name,
					'description': i.activity.description,
					'place': i.activity.place,
					'startTime': i.activity.startTime,
					'endTime': i.activity.endTime

				}
			)
		return showlist


class Barrage(models.Model):
	id = models.AutoField(primary_key=True)
	activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
	# user = models.ForeignKey(ActivityUser,on_delete=models.CASCADE)
	open_id = models.CharField(max_length=100)
	status = models.IntegerField()
	time = models.DateTimeField(default=timezone.now)
	OK = 1
	NOT_OK = 2
	TOP = 3
	class Meta:
		abstract = True


class Comment(Barrage):
	content = models.CharField(max_length=100)
	color = models.IntegerField()
	bolt = models.BooleanField()
	underline = models.BooleanField()
	incline = models.BooleanField()
	
	@staticmethod
	def insertComment(activity,open_id, content, color, bolt, underline, incline, time, status=Barrage.OK):
		comment = Comment(activity=activity,open_id=open_id, color=color, content=content, bolt=bolt, underline=underline, incline=incline,
		                  time=time, status=status)
		comment.save()
	
	@staticmethod
	def selectById(id):
		try:
			comment = Comment.objects.get(id=id)
		except Exception as e:
			logging.error(e)
			return None
		return comment
	
	@staticmethod
	def selectByActivityAndId(activity, id):
		comments = Comment.objects.filter(activity=activity).filter(id__gt=id)
		return comments


class Picture(Barrage):
	pic_url = models.ImageField(upload_to='', max_length=255)
	
	@staticmethod

	def insertComment(activity,open_id, pic_url, time, status=Barrage.OK):
		pic = Picture(activity=activity,open_id=open_id,pic_url=pic_url,
		                  time=time, status=status)
		pic.save()
	
	@staticmethod
	def selectById(id):
		try:
			pic = Picture.objects.get(id=id)
		except Exception as e:
			logging.error(e)
			return None
		return pic
	
	@staticmethod
	def selectByActivityAndId(activity, id):
		pics = Picture.objects.filter(activity=activity).filter(id__gt=id)
		return pics


class Lottery(models.Model):
	id = models.AutoField(primary_key=True)
	activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=100)
	first = models.IntegerField()
	second = models.IntegerField()
	third = models.IntegerField()
	special = models.IntegerField()
	status = models.IntegerField()
	PREPARING = 0
	RUNNING = 1
	FINISH = 2
	DELETE = 3
	
	@staticmethod
	def insertLottery(activity,name,description,first = 0,second = 0,third = 0,special = 0,status =PREPARING):
		lottery = Lottery(activity=activity,name=name,description=description,first=first,second=second,third=third,special=special,status=status)
		lottery.save()
		
	@staticmethod
	def selectById(id):
		try:
			lottery = Lottery.objects.get(id=id)
		except Exception as e:
			logging.error(e)
			return None
		return lottery
	
	@staticmethod
	def selectByActivity(activity):
		activities = Lottery.objects.filter(activity=activity)
		return activities
	
	@staticmethod
	def updateLottery(id,name,description,first = 0,second = 0,third = 0,special = 0,status =PREPARING):
		lottery = Lottery.selectById(id)
		if lottery is None:
			pass
		lottery.name = name
		lottery.description = description
		lottery.first = first
		lottery.second = second
		lottery.third  = third
		lottery.special = special
		lottery.status = status
		lottery.save()
	
	@staticmethod
	def deleteLottery(id):
		lottery = Lottery.selectById(id)
		if lottery is not None:
			lottery.status = Lottery.DELETE
		
	def running(self):
		if self.status != self.PREPARING:
			return False
		all_users = ActivityUser.objects.filter(activity=self.activity)
		df = pd.DataFrame(all_users)
		users = df.sample(n=self.first + self.second + self.third + self.special)
		lucky = []
		for indexs in users.index:
			lucky.append(users[0][indexs])
		count = 0
		for i in range(self.first):
			to_add = LotteryResult(open_id=lucky[count + i].open_id, lottery=self, prize=LotteryResult.FIRST)
			to_add.save()
		count += self.first
		for i in range(self.second):
			to_add = LotteryResult(open_id=lucky[i + count].open_id, lottery=self, prize=LotteryResult.SECOND)
			to_add.save()
		count += self.second
		for i in range(self.third):
			to_add = LotteryResult(open_id=lucky[i + count].open_id, lottery=self, prize=LotteryResult.THIRD)
			to_add.save()
		count += self.third
		for i in range(self.special):
			to_add = LotteryResult(open_id=lucky[i + count].open_id, lottery=self, prize=LotteryResult.SPECIAL)
			to_add.save()
		self.status = self.FINISH
		return True
	
	def getResult(self):
		pass


class LotteryResult(models.Model):
	open_id = models.CharField(max_length=100)
	lottery = models.ForeignKey(Lottery, on_delete=models.CASCADE)
	prize = models.IntegerField()
	FIRST = 1
	SECOND = 2
	THIRD = 3
	SPECIAL = 4
