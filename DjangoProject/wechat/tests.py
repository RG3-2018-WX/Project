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
    def test_user_activity_list_exist(self):
        c = Client()
        d = c.get('/api/u/activity/list/',{'openId':'111'})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(json_text['data'][0][name],'PREPARING ACTIVITY')
        self.assertEqual(json_text['code'], 0)

    @before_test
    def test_user_activity_list_not_exist(self):
        c = Client()
        d = c.get('/api/u/activity/list/', {'openId': '333'})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertNotEqual(json_text['code'], 0)

    @before_test
    def test_user_activity_detail_exist(self):
        c = Client()
        d = c.get('/api/u/activity/detail/', {'activityId': '1'})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(json_text['data'][0][name], 'prog 1 1')
        self.assertEqual(json_text['code'], 0)



    @before_test
    def test_user_activity_detail_not_exist(self):
        c = Client()
        d = c.get('/api/u/activity/detail/', {'activityId': '333'})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertNotEqual(json_text['code'], 0)

    @before_test
    def test_user_program_exist(self):
        c = Client()
        d = c.get('/api/u/activity/program/', {'activityId': '1','sequence':'2'})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(json_text['data'][0][name], 'prog 1 2')
        self.assertEqual(json_text['code'], 0)
    @before_test
    def test_user_program_not_exist(self):
        c = Client()
        d = c.get('/api/u/activity/program/', {'activityId': '333'})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertNotEqual(json_text['code'], 0)

    @before_test
    def test_user_lottery_exist(self):
        c = Client()
        d = c.get('/api/u/lottery/list/', {'activityId': '1', 'openId': '111'})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(json_text['data'][0][name], 'lottery 1 1')
        self.assertEqual(json_text['code'], 0)

    @before_test
    def test_user_lottery_not_exist(self):
        c = Client()
        d = c.get('/api/u/lottery/list/', {'activityId': '1', 'openId': '3333'})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertNotEqual(json_text['code'], 0)

    @before_test
    def test_user_setcomment(self):
        c = Client()
        d = c.get('/api/u/activity/comment/', {'activityId': '1', 'content': '111','openId':'111',
                                               'color':'212','bolt':'0','incline':'0','underline':'0'})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(json_text['code'], 0)

    @before_test
    def test_login_post_succeed(self):
        c = Client()
        d = c.post('/api/a/login/', {'username': 'admin', 'password': '123456'})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertEqual(json_text['code'], 0)

    @before_test
    def test_register_post_succeed(self):
        c = Client()
        d = c.post('/api/a/register/',{'username':'admin1','password':'1234567'})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertEqual(json_text['code'], 0)

    @before_test
    def test_register_post_not_succeed(self):
        c = Client()
        d = c.post('/api/a/register/', {'username': 'admin', 'password': '123456'})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertNotEqual(json_text['code'], 0)

    @before_test
    def test_login_post_not_succeed(self):

        c = Client()
        d = c.post('/api/a/login/', {'username': 'admin', 'password': '1234567'})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertNotEqual(json_text['code'], 0)

    @before_test
    def test_logout_post_succeed(self):

        c = Client()
        print(c.cookies)
        d = c.post('/api/a/login/', {'username': 'admin', 'password': '123456'})
        print(c.cookies)
        d =  c.POST('/api/a/logout/',{})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code,200)
        self.assertEqual(json_text['code'],0)

    @before_test
    def test_logout_post_not_succeed(self):

        c = Client()
        d = c.post('/api/a/logout/',{})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code,200)
        self.assertNotEqual(json_text['code'],0)

    @before_test
    def test_login_get_not_exist(self):

        c = Client()
        d = c.get('/api/a/login/', {})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertNotEqual(json_text['code'], 0)

    @before_test
    def test_activity_list_get(self):

        c = Client()
        d = c.get('/api/a/activity/list', {})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertEqual(json_text['data'][0]['activityId'],1)

    @before_test
    def test_activity_create_succeed(self):
        c = Client()
        d = c.post("/api/a/activity/create/", {
            'name': '2',
            'place': 'place',
            'description': 'description',
            'picUrl': 'url',
            'startTime': '1000000000',
            'endTime': '1000000100',
            'organizer':'admin',
            'bgPicUrl':'burl',
            'status': 0})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertEqual(json_text['code'], 0)

    @before_test
    def test_activity_create_not_succeed(self):

        c = Client()
        d = c.post("/api/a/activity/create/", {})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertNotEqual(json_text['code'], 0)

    @before_test
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

    @before_test
    def test_image_upload_not_succeed(self):

        c = Client()
        d = c.post('/api/a/image/upload/', {})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertNotEqual(json_text['code'], 0)

    @before_test
    def test_activity_detail_get_succeed(self):

        c = Client()
        d = c.get('/api/a/activity/detail/', {'activityId': 1})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertEqual(json_text['data']['name'],'PREPARING ACTIVITY')

    @before_test
    def test_activity_detail_get_not_succeed(self):
        c = Client()
        d = c.post('/api/a/activity/detail/', {'activityId':3})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertNotEqual(json_text['code'], 0)

    @before_test
    def test_activity_detail_post_succeed(self):
        c = Client()
        d = c.post("/api/a/activity/detail/", {
            'activityId':'1',
            'name': '3',
            'place': 'blace',
            'description': 'eescription',
            'picUrl': 'durl',
            'startTime': '01000000000',
            'endTime': '01000000100',
            'organizer': '0admin',
            'bgPicUrl': '0burl',
            'status': 0})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertEqual(json_text['code'], 0)

    @before_test
    def test_activity_detail_post_not_succeed(self):
        c = Client()
        d = c.post("/api/a/activity/detail/", {})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertNotEqual(json_text['code'], 0)

    @before_test
    def test_lottery_list_get(self):
        c = Client()
        d = c.get('/api/a/lottery/list', {'activityId':'1'})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertEqual(json_text['data'][0]['name'], 'lottery 1 1')

    @before_test
    def test_lottery_create_succeed(self):
        c = Client()
        d = c.post("/api/a/lottery/create/", {
            'name': '2',
            'activityId': '1',
            'first':1,
            'second':1,
            'third':1,
            'special':1,
            'status': 0})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertEqual(json_text['code'], 0)

    @before_test
    def test_lottery_create_not_succeed(self):

        c = Client()
        d = c.post("/api/a/lottery/create/", {})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertNotEqual(json_text['code'], 0)


    @before_test
    def test_lottery_detail_get_succeed(self):

        c = Client()
        d = c.get('/api/a/lottery/detail/', {'lotteryId': 1})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertEqual(json_text['data']['name'], 'lottery 1 1')

    @before_test
    def test_lottery_detail_get_not_succeed(self):
        c = Client()
        d = c.post('/api/a/lottery/detail/', {'lotteryId': 3})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertNotEqual(json_text['code'], 0)

    @before_test
    def test_lottery_detail_post_succeed(self):
        c = Client()
        d = c.post("/api/a/lottery/detail/", {
            'name': '3',
            'activityId': '1',
            'first': 1,
            'second': 1,
            'third': 1,
            'special': 1,
            'status': 0})

        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertEqual(json_text['code'], 0)

    @before_test
    def test_lottery_detail_post_not_succeed(self):

        c = Client()
        d = c.post("/api/a/lottery/detail/", {})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertNotEqual(json_text['code'], 0)

    @before_test
    def test_program_list_get(self):
        c = Client()
        d = c.get('/api/a/program/list', {'activityId': '12'})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertNotEqual(json_text['code'], 0)

    @before_test
    def test_program_list_not_succeed(self):

        c = Client()
        d = c.get("/api/a/program/create/", {})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertNotEqual(json_text['code'], 0)
    @before_test
    def test_program_create_succeed(self):
        c = Client()
        d = c.post("/api/a/program/create/", {
            'name': '2',
            'activityId': '1',
            'description': 'desc 1 3',
            'actors':'dwd',
            'sequence': 3})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertEqual(json_text['code'], 0)

    @before_test
    def test_program_create_not_succeed(self):

        c = Client()
        d = c.post("/api/a/program/create/", {})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertNotEqual(json_text['code'], 0)

    @before_test
    def test_program_detail_get_succeed(self):

        c = Client()
        d = c.get('/api/a/program/detail/', {'programId': 1})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertEqual(json_text['data']['name'], 'prog 1 1')

    @before_test
    def test_program_detail_get_not_succeed(self):
        c = Client()
        d = c.post('/api/a/program/detail/', {'programId':32 })
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertNotEqual(json_text['code'], 0)

    @before_test
    def test_program_detail_post_succeed(self):
        c = Client()
        d = c.post("/api/a/program/detail/", {
            'name': 'dsfwef',
            'programId': '1',
            'sequence': 1,
            'actors': 'qwewwef',
            'description': '12323'})


        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertEqual(json_text['code'], 0)

    @before_test
    def test_lottery_detail_post_not_succeed(self):

        c = Client()
        d = c.post("/api/a/lottery/detail/", {})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertNotEqual(json_text['code'], 0)
    @before_test
    def test_comment_set_linenumber_succeed(self):
        c = Client()
        d = c.post("/api/a/comment/linenumber/", {'commentLinebumber':'4'})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertEqual(json_text['code'], 0)

    def test_comment_set_linenumber_not_succeed(self):
        c = Client()
        d = c.post("/api/a/comment/linenumber/", { })
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertNotEqual(json_text['code'], 0)

    @before_test
    def test_barrage_comment_set_linenumber_succeed(self):
        c = Client()
        d = c.get("/api/c/comment/linenumber/", )
        if d.status_code == 404:
            return
        json_text = json.loads(d.content.decode('utf-8'))
        self.assertEqual(d.status_code, 200)
        self.assertEqual(json_text['code'], 0)

# @before_test

# Create your tests here.
