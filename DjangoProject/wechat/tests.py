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
	
	def test_user_bind_post_exsit(self):
		self.before_test()
		user = MyUser(open_id='2', student_id="1234567890")
		user.save()
		c = Client()
		d = c.post('/api/u/user/bind/', {'openid': '2', 'student_id': '2016013238', 'password': "123456"})
		if d.status_code == 404:
			return
		self.assertEqual(d.status_code, 200)
		json_text = json.loads(d.content.decode('utf-8'))
		self.assertEqual(json_text['code'], 0)
		
		c = Client()
		d = c.get('/api/u/user/bind/', {'openid': '2'})
		if d.status_code == 404:
			return
		json_text = json.loads(d.content.decode('utf-8'))
		self.assertEqual(json_text['data'], '2016013238')
	
	def test_user_bind_post_not_exist(self):
		self.before_test()
		c = Client()
		d = c.post('/api/u/user/bind/', {'openid': '2', 'student_id': '2016013238', 'password': "123456"})
		if d.status_code == 404:
			return
		self.assertEqual(d.status_code, 200)
		json_text = json.loads(d.content.decode('utf-8'))
		self.assertNotEqual(json_text['code'], 0)
	
	def test_activity_detail_get_exist(self):
		self.before_test()
		c = Client()
		d = c.get('/api/u/activity/detail/', {'id': 1})
		if d.status_code == 404:
			return
		json_text = json.loads(d.content.decode('utf-8'))
		self.assertEqual(json_text['data']['key'], '1-key')
		self.assertEqual(json_text['code'], 0)
	
	def test_activity_detail_get_not_exist(self):
		self.before_test()
		c = Client()
		d = c.get('/api/u/activity/detail/', {'id': 100})
		if d.status_code == 404:
			return
		json_text = json.loads(d.content.decode('utf-8'))
		self.assertEqual(d.status_code, 200)
		self.assertNotEqual(json_text['code'], 0)
	
	def test_ticket_detail_get_exist(self):
		self.before_test()
		c = Client()
		d = c.get('/api/u/ticket/detail/', {'openid': '1', 'ticket': 1})
		if d.status_code == 404:
			return
		
		json_text = json.loads(d.content.decode('utf-8'))
		print("json test:")
		print(json_text)
		self.assertEqual(d.status_code, 200)
		
		self.assertEqual(json_text['data']['activityKey'], '1-key')
	
	def test_login_post_succeed(self):
		self.before_test()
		c = Client()
		d = c.post('/api/a/login/', {'username': 'admin', 'password': 'xxd123456'})
		if d.status_code == 404:
			return
		json_text = json.loads(d.content.decode('utf-8'))
		self.assertEqual(d.status_code, 200)
		self.assertEqual(json_text['code'], 0)
	
	def test_login_post_not_succeed(self):
		self.before_test()
		c = Client()
		
		d = c.post('/api/a/login/', {'username': 'admin', 'password': '1234567'})
		if d.status_code == 404:
			return
		json_text = json.loads(d.content.decode('utf-8'))
		self.assertEqual(d.status_code, 200)
		self.assertNotEqual(json_text['code'], 0)
		
		'''    def test_logout_post_succeed(self):
		self.before_test()
		c = Client()
		print(c.cookies)
		d = c.post('/api/a/login/', {'username': 'admin', 'password': 'xxd123456'})
		print(c.cookies)
		d =  c.POST('/api/a/logout/',{})
		if d.status_code == 404:
			return
		json_text = json.loads(d.content.decode('utf-8'))
		self.assertEqual(d.status_code,200)
		self.assertEqual(json_text['code'],0)


	def test_logout_post_not_succeed(self):
		self.before_test()
		c = Client()
		d = c.post('/api/a/logout/',{})
		if d.status_code == 404:
			return
		json_text = json.loads(d.content.decode('utf-8'))
		self.assertEqual(d.status_code,200)
		self.assertNotEqual(json_text['code'],0)
'''
	
	def test_login_get_not_exist(self):
		self.before_test()
		c = Client()
		d = c.get('/api/a/login/', {})
		if d.status_code == 404:
			return
		json_text = json.loads(d.content.decode('utf-8'))
		self.assertNotEqual(json_text['code'], 0)
	
	def test_activity_list_get(self):
		self.before_test()
		c = Client()
		d = c.get('/api/a/activity/list', {})
		if d.status_code == 404:
			return
		json_text = json.loads(d.content.decode('utf-8'))
		self.assertEqual(d.status_code, 200)
	
	# self.assertEqual(json_text['data'][0]['id'],1)
	
	def test_activity_delete_succeed(self):
		self.before_test()
		c = Client()
		d = c.get('/api/a/activity/delete/', {'id': 1})
		if d.status_code == 404:
			return
		json_text = json.loads(d.content.decode('utf-8'))
		self.assertEqual(d.status_code, 200)
		self.assertEqual(json_text['code'], 0)
	
	def test_activity_delete_not_succeed(self):
		self.before_test()
		c = Client()
		d = c.get('/api/a/activity/delete/', {'id': 1})
		d = c.get('/api/a/activity/delete/', {'id': 1})
		if d.status_code == 404:
			return
		json_text = json.loads(d.content.decode('utf-8'))
		self.assertEqual(d.status_code, 200)
		self.assertNotEqual(json_text['code'], 0)
	
	def test_activity_create_succeed(self):
		self.before_test()
		c = Client()
		d = c.post("/api/a/activity/create/", {
			'name': '2',
			'key': '2-key',
			'place': 'place',
			'description': 'description',
			'picUrl': 'url',
			'startTime': '1000000000',
			'endTime': '1000000100',
			'bookStart': '999999900',
			'bookEnd': '999999990',
			'totalTickets': 100,
			'status': 0})
		if d.status_code == 404:
			return
		json_text = json.loads(d.content.decode('utf-8'))
		self.assertEqual(d.status_code, 200)
		self.assertEqual(json_text['code'], 0)
		self.assertEqual(json_text['data'], 2)
	
	def test_activity_create_not_succeed(self):
		self.before_test()
		c = Client()
		d = c.post("/api/a/activity/create/", {})
		if d.status_code == 404:
			return
		json_text = json.loads(d.content.decode('utf-8'))
		self.assertEqual(d.status_code, 200)
		self.assertNotEqual(json_text['code'], 0)
	
	def test_image_upload_succeed(self):
		self.before_test()
		c = Client()
		d = c.post('/api/a/image/upload/', {})
		if d.status_code == 404:
			return
		json_text = json.loads(d.content.decode('utf-8'))
		self.assertEqual(d.status_code, 200)
		self.assertEqual(json_text['code'], 0)
	
	# self.assertEqual(json_text['data'],)
	
	def test_image_upload_not_succeed(self):
		self.before_test()
		c = Client()
		d = c.post('/api/a/image/upload/', {})
		if d.status_code == 404:
			return
		json_text = json.loads(d.content.decode('utf-8'))
		self.assertEqual(d.status_code, 200)
		self.assertNotEqual(json_text['code'], 0)
	
	def test_activity_detail_get(self):
		self.before_test()
		c = Client()
		d = c.get('/api/a/activity/detail/', {'id': 1})
		if d.status_code == 404:
			return
		json_text = json.loads(d.content.decode('utf-8'))
		self.assertEqual(d.status_code, 200)
	
	# self.assertEqual()#deal with get data
	
	def test_activity_menu_get(self):
		self.before_test()
		c = Client()
		d = c.get('/api/a/activity/menu/', {})
		if d.status_code == 404:
			return
		self.assertEqual(d.status_code, 200)
	
	# self.assertEqual()#check data
	
	def test_activity_menu_post_succeed(self):
		pass
	
	def test_activity_menu_post_not_succeed(self):
		pass
	
	def test_checkin_post_succeed(self):
		self.before_test()
		c = Client()
		d = c.get('/api/a/activity/checkin/', {'actid': 1, 'ticket': 1})
		if d.status_code == 404:
			return
		json_text = json.loads(d.content.decode('utf-8'))
		self.assertEqual(d.status_code, 200)
		self.assertEqual(json_text['data']['student'], 1)
		self.assertNotEqual(json_text['code'], 0)  # check data
	
	def test_checkin_post_not_succeed(self):
		self.before_test()
		c = Client()
		d = c.get('/api/a/activity/checkin/', {'actid': 2, 'ticket': 2})
		if d.status_code == 404:
			return
		json_text = json.loads(d.content.decode('utf-8'))
		self.assertEqual(d.status_code, 200)
		
		self.assertNotEqual(json_text['code'], 0)
# check data
# Create your tests here.
