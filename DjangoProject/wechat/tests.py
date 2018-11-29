import json

from django.test import TestCase
from DjangoProject.models import *
from django.test import Client
from django.utils import timezone

from django.contrib.auth.models import User
from django.contrib.auth import login


class WechatTest(TestCase):
	
	def before_test(self):
		a = User.objects.create_user(username='admin', password='123456', email='example@163.com')
		a.save()
		
		Activity.insertActivity(a, 'desc prep', '', timezone.now(), timezone.now(), '', Activity.PREPARING, 'place',
		                        'PREPARING ACTIVITY')
		Activity.insertActivity(a, 'desc run', '', timezone.now(), timezone.now(), '', Activity.RUNNING, 'place',
		                        'RUNNING ACTIVITY')
		
		activity_list = Activity.selectByOrganizer(a)
		self.activity_1 = activity_list[0]
		self.activity_2 = activity_list[1]
		Programe.insertPrograme(self.activity_1, 'prog 1 1', 'desc 1 1', 1, 'actors 1 1')
		Programe.insertPrograme(self.activity_1, 'prog 1 2', 'desc 1 2', 2, 'actors 1 2')
		Programe.insertPrograme(self.activity_2, 'prog 2 1', 'desc 2 1', 1, 'actors 2 1')
		Programe.insertPrograme(self.activity_2, 'prog 2 2', 'desc 2 2', 2, 'actors 2 2')
		
		ActivityUser.insertActivityUser('111', self.activity_1)
		ActivityUser.insertActivityUser('222', self.activity_2)
		
		Lottery.insertLottery(self.activity_1, 'lottery 1 1', 'desc 1 1', 1, 1, 1, 1)
	
	@before_test
	def test_lottery_running(self):
		lottery = Lottery.selectByActivity(self.activity_1)[0]
		lottery.running()
	
	@before_test
	def test_(self):
		c = Client()
		d = c.get('/api/u/user/bind/', {'openid': '1'})
		if d.status_code == 404:
			return
		json_text = json.loads(d.content.decode('utf-8'))
		self.assertEqual(json_text['data'], '2016013237')
		
	#@before_test
	
# Create your tests here.
