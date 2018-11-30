from django.shortcuts import render
from codex.baseerror import *
from codex.baseview import APIView
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth import logout

from DjangoProject import models
from DjangoProject.models import Activity, Ticket, Organizer, Lottery, Programe,Barrage,Comment,Picture
from django.utils import timezone
from wechat.views import CustomWeChatView
import uuid
from WeChatTicket import settings
import os


class Login(APIView):
    def get(self):
        print("Login Get")
        if not self.request.user.is_authenticated():
            raise ValidateError("Please Login!")

    def post(self):
        self.check_input('username', 'password')
        user = authenticate(username=self.input['username'], password=self.input['password'])
        if user is not None and user.is_active:
            login(self.request, user)
            return
        if not User.objects.filter(username=self.input['username']):
            raise ValidateError("Username not exist")

        raise ValidateError("wrong password")


class Register(APIView):
    def post(self):
        self.check_input('username', 'password')
        if User.objects.get(username=self.input['username']):
            raise ValidateError('The username has been occupied')
        else:
            user = User.objects.create_user(username=self.input['username'], password=self.input['password'],
                                            email='example@163.com')
            user.save()
        if not User.objects.get(self.input['username']):
            raise ValidateError('register failed')


class Logout(APIView):

    def post(self):
        print("Log out Post")
        if not self.request.user.is_authenticated():
            raise LogicError('no user is online')
        else:
            logout(self.request)


class ActivityList(APIView):
    def get(self):
        if not self.request.user.is_authenticatedd():
            raise ValidateError("Please Login First!")
        list = Activity.selectByOrganizer(self.request.user.username)
        output_list = []
        for i in list:
            output_list.append({
                'activityId': i.id,
                'name': i.name,
                'startTime': i.start_time.timestamp(),
                'endTime': i.end_time.timestamp(),
            })
        return output_list


class ActivityDelete(APIView):
    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        self.check_input('activityId')
        activity = Activity.selectById(self.input['activityId'])
        if activity:
            activity.deleteActivity()
        else:
            raise LogicError('no such activity')


class ActivityStatus(APIView):
    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        self.check_input('activityId', 'status')
        activity = Activity.selectById(self.input['activityId'])
        if activity:
            activity.status = self.input['status']
            activity.save()
        else:
            raise LogicError('no such activity')


class ActivityCreate(APIView):

    def post(self):

        if not self.request.user.is_authenticated():
            raise ValidateError("Please Login First!")
        self.check_input("name", "place", "description", "picUrl", "bgPicUrl", "startTime",
                         "endTime", "status", "organizer")
        Activity.insertActivity(self.input['organizer'], self.input['description'], self.input['picUrl'],
                                self.input['startTime'], self.input['endTime'],
                                self.input['bgPicUrl'], self.input['status'], self.input['palce'], self.input['name'])
        if not Activity.objects.get(self.input['name']):
            raise LogicError()


class ImageUpload(APIView):

    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        self.check_input("image")
        try:
            image = self.input["image"][0]

            name = str(uuid.uuid1()) + image.name
            file = open('./static/pic/' + name, 'wb')
            for chunk in image.chunks():
                file.write(chunk)
            file.close()
            path = 'pic/' + name
            self.url = os.path.join(settings.CONFIGS["SITE_DOMAIN"], path)


        except:
            raise ValidateError()

    def get(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        return self.url


class ActivityDetail(APIView):
    def get(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        self.check_input('activityId')
        activity = Activity.selectById(self.input['activityId'])
        if activity:
            data = {'name': activity.name,
                    'description': activity.description,
                    'startTime': activity.start_time.timestamp(),
                    'endTime': activity.end_time.timestamp(),
                    'place': activity.place,
                    'picUrl': activity.pic_url,
                    'bgPicUrl': activity.bg_pic_url,
                    'organizer': activity.organizer,
                    'status': activity.status
                    }

            return data
        else:
            raise InputError()

    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        self.check_input('activityId')
        activity = Activity.selectById['activityId']
        old_activity = activity
        if activity:
            if activity.status == 0:
                Activity.updateActivity(self.input['activityId'],self.input['organizer'], self.input['description'],
                                        self.input['picUrl'],
                                        self.input['startTime'], self.input['endTime'],
                                        self.input['bgPicUrl'], self.input['status'], self.input['palce'],
                                        self.input['name'])
            elif activity.status == 1:
                raise InputError('the activity already start')

        else:
            raise ValidateError('no such activity')
        activity.save()
        return 0


class LotteryCreate(APIView):
    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        self.check_input("name", "description", "activityId", "first",
                         "second", "status", "speical", 'third')
        obj = Lottery(name=self.input['name'],
                      activity=Activity.selectById(self.input['activityId']),
                      description=self.input['description'],
                      first=self.input['first'],
                      status=self.input['status'],
                      second=self.input['second'],
                      third=self.input['third'],
                      speical=self.input['speical'],

                      )
        obj.save()

        if not Lottery.objects.get(self.input['name']):
            raise LogicError('lottery creat failed')


class LotteryDetail(APIView):
    def get(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        self.check_input('id')
        lottery = Lottery.objects.get(Lotter=self.input('id'))
        if lottery:
            data = {'name': lottery.name,
                    'description': lottery.description,
                    'speical': lottery.special,
                    'first': lottery.first,
                    'second': lottery.second,
                    'third': lottery.third,
                    'status': activity.status
                    }

            return data
        else:
            raise InputError()

    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        self.check_input("name", "description", "activityId", "first",
                         "second", "status", "speical", 'third', 'id')
        lottery = Lottery.objects.get(id=self.input('id'))
        old_lottery = lottery
        if lottery:
            if lottery.status == lottery.PREPARING:
                lottery.lottery.name = self.input['name'],
                lottery.activity = Activity.selectById(self.input['activityId']),
                lottery.description = self.input['description'],
                lottery.first = self.input['first'],
                lottery.status = self.input['status'],
                lottery.second = self.input['second'],
                lottery.third = self.input['third'],
                lottery.speical = self.input['speical'],
                lottery.id = self.input['id']
            else:
                raise ValidateError('the lottery is runing or finished')
        else:
            raise ValidateError('no such lottery')

        lottery.save()


class LotteryDelete(APIView):
    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        self.check_input('id')
        lottery = Lottery.objects.get(id=self.input[id])
        if lottery:
            lottery.status = Lottery.DELETE
        else:
            raise LogicError('no such activity')


class LotteryStatus(APIView):
    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        self.check_input('id', 'status')
        lottery = Lottery.objects.get(id=self.input[id])
        if lottery:
            lottery.status = self.input['status']
            lottery.save()
        else:
            raise LogicError('no such activity')

class LotteryList(APIView):
    def get(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        self.check_input('activityId')
        lottery_list=Lottery.objects.filter(activity__id=self.input['activityId'])
        if not lottery_list:
            raise InputError('no such activity')
        list = []
        for lottery in lottery_list:
            list.append({
                'name':lottery.name,
                'status':lottery.status
            })
        return list
class ProgrameList(APIView):
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


class ProgrameDelete(APIView):
    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        self.check_input('programId')
        Programe.deletePrograme(self.input['programId'])




class ProgrameCreate(APIView):

    def post(self):

        if not self.request.user.is_authenticated():
            raise ValidateError("Please Login First!")
        self.check_input('activityId', 'name', 'description', 'sequence', 'actors')
        Programe.insertPrograme(Activity.selectById(self.input['activityId']), self.input['name'],
                                self.input['description']
                                , self.input['sequence'], self.input['actors'])
        if not Activity.objects.get(self.input['name']):
            raise LogicError('fail creat pragram')


class ProgrameDetail(APIView):
    def get(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        self.check_input('programId')
        programe = Programe.selectById(self.input['programId'])
        if programe:
            data = {'name': programe.name,
                    'description': programe.description,
                    'sequence': programe.sequence,
                    'actors': programe.actors
                    }

            return data
        else:
            raise InputError('no such programe')

    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        self.check_input('programId')
        programe = Programe.selectById['programId']
        old_programe = programe
        if programe:
            programe.updatePrograme(self.input['programId'], self.input['name'],
                                    self.input['description']
                                    , self.input['actors'], self.input['sequence'])

        else:
            raise ValidateError('no such program')
        programe.save()
        if old_programe == programe:
            raise InputError('no change!')
        else:
            return 0


class SetCommentLinenumber(APIView):
    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        self.check_input('commentLinenumber')
        return self.input['commentLinenumber']

class SetTop(APIView):
    def post(self):
        self.check_input('activityId')
        old_top = Comment.objects.get(status = Barrage.TOP)
        old_top.status = Barrage.NOT_OK
        old_top.save()
        Comment.insertComment(Activity.selectById(self.input['activityId']),self.request.user.username,self.input['color'],self.input['content'],
            self.input['bolt'], self.input['underline'] ,self.input['incline'],timezone.now(),Barrage.TOP)

class SetComment(APIView):
    def get(self):
        self.check_input('activityId','commentId')
        show_list=[]
        comment_list = Comment.objects.filter(time__lt=timezone.now().time.second).filter(id__gt=self.input['commentId'])
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
        pic_list = Comment.objects.filter(time__lt=timezone.now().time.second ).filter(id__gt=self.input['pictureId'])
        for pic in pic_list:
            show_list.append(
                {
                    'id':pic.id,
                    'picUrl': pic.pic_url
                }
            )

        return show_list
class CommentStatus(APIView):
    def post(self):
        self.check_input('id','status')
        comment = Comment.selectById(self.input['id'])
        if comment:
            comment.status = self.input['status']
            comment.save()
        comment = Picture.selectById(self.input['id'])
        if comment:
            comment.status = self.input['status']
            comment.save()
        if not comment:
            return InputError('no such comment')
# Create your views here.
