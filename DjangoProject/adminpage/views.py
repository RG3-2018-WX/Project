from django.shortcuts import render
from codex.baseerror import *
from codex.baseview import APIView
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.shortcuts import render, redirect, HttpResponse
from django.utils.timezone import now, timedelta
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse

from DjangoProject import models
from DjangoProject.models import Activity, Lottery, Programe, Barrage, Comment, Picture
from django.utils import timezone
from wechat.views import CustomWeChatView
import uuid
from DjangoProject import settings
import os
import time

num = 0

class Login(APIView):
    def get(self):
        print("Login Get")
        if not self.request.user.is_authenticated():
            #raise ValidateError("Please Login!")
            return {'view': 26}

        return {'view': 26}

    def post(self):
        if 'login' in self.request.POST:
            self.check_input('username', 'password')
            user = authenticate(username=self.input['username'], password=self.input['password'])
            if user is not None and user.is_active:
                login(self.request, user)
                return {'view': 27}
            if not User.objects.filter(username=self.input['username']):
                #raise ValidateError("Username not exist")
                messages.success(self.request, "Username not exist")
                return {'view': 2, 'username': self.input['username'], 'password': self.input['password']}

            #raise ValidateError("wrong password")
            messages.success(self.request, "wrong password")
            return {'view': 2, 'username': self.input['username'], 'password': self.input['password']}
        
        if 'register' in self.request.POST:
            self.check_input('username', 'password')
            if User.objects.filter(username=self.input['username']):
                #raise ValidateError('The username has been occupied')
                #return {'view': 5, 'msg': 'The username has been occupied'}
                messages.success(self.request, "The username has been occupied")
                return {'view': 2, 'username': self.input['username'], 'password': self.input['password']}
            else:
                user = User.objects.create_user(username=self.input['username'], password=self.input['password'])
                if user is False:
                    #raise ValidateError('register failed')
                    #return {'view': 5, 'msg': 'register failed'}
                    messages.success(self.request, "register failed")
                    return {'view': 2, 'username': self.input['username'], 'password': self.input['password']}
                else:
                    #return {'view': 5, 'msg': 'registration success'}
                    messages.success(self.request, "registration success")
                    return {'view': 2, 'username': self.input['username'], 'password': self.input['password']}


'''class Register(APIView):
    def get(self):
        print("Login Get")
        if not self.request.user.is_authenticated():
            #raise ValidateError("Please Login!")
            return {'view': 3}
        
        return {'view': 3}
    
    def post(self):
        if 'register' in self.request.POST:
            self.check_input('username', 'password')
            #if User.objects.get(username=self.input['username']):
                #raise ValidateError('The username has been occupied')
                #return {'view': 5, 'msg': 'The username has been occupied'}
            #else:
            user = User.objects.create_user(username=self.input['username'], password=self.input['password'])
            if user is False:
                #raise ValidateError('register failed')
                return {'view': 5, 'msg': 'register failed'}
            else:
                return {'view': 5, 'msg': 'registration success'}
            
        else:
            return {'view': 0}'''


class Logout(APIView):
    def get(self):
        print("Log out Post")
        #if not self.request.user.is_authenticated():
            #raise LogicError('no user is online')
        #else:
        logout(self.request)
        return {'view': 4}


class ActivityList(APIView):
    def get(self):
        print("Activity Get")
        if not self.request.user.is_authenticated():
            return {'view': 0}
        list = Activity.selectByOrganizer(self.request.user)
        output_list = []
        for i in list:
            output_list.append({
                'activityId': i.id,
                'name': i.name,
                'startTime': i.start_time,
                'endTime': i.end_time,
                'place': i.place,
                'status': i.status
            })
        return {'view': 7, 'msg': output_list}
    
    def post(self):
        if 'create' in self.request.POST:
            #return redirect('/a/Activity/create/')
            return {'view': 11}

        if 'logout' in self.request.POST:
            return {'view': 0}


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


class ActivityDelete(APIView):
    def get(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        nid = self.request.GET.get('nid')
        Activity.deleteActivity(nid)
        return {'view': 27}


class ActivityCreate(APIView):
    def get(self):
        print("Activity Create Get")
        if not self.request.user.is_authenticated():
            return {'view': 0}
        return {'view': 12}

    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please Login First!")
        if 'create' in self.request.POST:
            self.check_input("name", "place", "description", "picUrl", "bgPicUrl", "startTime",
                             "endTime")
            #img = self.request.FILES.get('picUrl')
            Activity.insertActivity(self.request.user, self.input['description'], self.input['picUrl'][0],
                                    self.input['startTime'], self.input['endTime'], self.input['bgPicUrl'][0],
                                    0, self.input['place'], self.input['name'])
            #if not Activity.objects.get(self.input['name']):
                #raise LogicError()
            #else:
            return {'view': 27}
            
        if 'return' in self.request.POST:
            return {'view': 27}


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
        #self.check_input('activityId')
        #activity = Activity.selectById(self.input['activityId'])
        nid = self.request.GET.get('nid')
        activity = Activity.selectById(nid)
        if activity:
            data = {'name': activity.name,
                    'description': activity.description,
                    'startTime': activity.start_time,
                    'endTime': activity.end_time,
                    'place': activity.place,
                    'picUrl': activity.pic_url,
                    'bgPicUrl': activity.bg_pic_url,
                    'organizer': activity.organizer,
                    'status': activity.status
                    }
            
            return {'view': 13, 'name': activity.name, 'description': activity.description,
                           'startTime': activity.start_time.isoformat()[:-6], 'endTime': activity.end_time.isoformat()[:-6],
                           'place': activity.place, 'picUrl': activity.pic_url, 'bgPicUrl': activity.bg_pic_url,
                           'organizer': activity.organizer, 'status': activity.status, 'acitivityid': nid}
        else:
            raise InputError()

    def post(self):
        nid = self.request.GET.get('nid')
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        
        if 'edit' in self.request.POST:
            activity = Activity.selectById(nid)
            old_activity = activity
            if activity:
                if self.input['picUrl'] == "":
                    picUrl = activity.pic_url
                else:
                    picUrl = self.input['picUrl'][0]
                if self.input['bgPicUrl'] == "":
                    bgPicUrl = activity.bg_pic_url
                else:
                    bgPicUrl = self.input['bgPicUrl'][0]
                Activity.updateActivity(nid, self.request.user, self.input['description'],
                                        picUrl,
                                            self.input['startTime'], self.input['endTime'],
                                        bgPicUrl, activity.status, self.input['place'],
                                            self.input['name'])

            else:
                raise ValidateError('no such activity')
            # return 0
            return {'view': 27}
        
        if 'return' in self.request.POST:
            return {'view': 27}
        
        if 'begin' in self.request.POST:
            Activity.updateActivity(nid, self.request.user, self.input['description'],
                                            self.input['picUrl'],
                                            self.input['startTime'], self.input['endTime'],
                                            self.input['bgPicUrl'], 1, self.input['place'],
                                            self.input['name'])
            activity = Activity.selectById(nid)
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
            
                return {'view': 13, 'name': activity.name, 'description': activity.description,
                           'startTime': activity.start_time, 'endTime': activity.end_time,
                           'place': activity.place, 'picUrl': activity.pic_url, 'bgPicUrl': activity.bg_pic_url,
                           'organizer': activity.organizer, 'status': activity.status, 'acitivityid': nid}
            #return {'view': 18}
        
        if 'end' in self.request.POST:
            Activity.updateActivity(nid,self.request.user, self.input['description'],
                                            self.input['picUrl'],
                                            self.input['startTime'], self.input['endTime'],
                                            self.input['bgPicUrl'], 2, self.input['place'],
                                            self.input['name'])
            activity = Activity.selectById(nid)
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
            
                return {'view': 13, 'name': activity.name, 'description': activity.description,
                           'startTime': activity.start_time, 'endTime': activity.end_time,
                           'place': activity.place, 'picUrl': activity.pic_url, 'bgPicUrl': activity.bg_pic_url,
                           'organizer': activity.organizer, 'status': activity.status, 'acitivityid': nid}
            #return {'view': 18}
        
        if 'detail' in self.request.POST:
            nid = self.get().get('nid')
            Activity.objects.filter(activityId=nid)
            return {'view': 25}


class Activitys(APIView):
    def get(self):
        #self.check_input('activityId')
        #activity = Activity.selectById(self.input['activityId'])
        nid = self.request.GET.get('nid')
        activity = Activity.selectById(nid)
        if activity:
            data = {'name': activity.name,
                    'description': activity.description,
                    'startTime': activity.start_time,
                    'endTime': activity.end_time,
                    'place': activity.place,
                    'picUrl': activity.pic_url,
                    'bgPicUrl': activity.bg_pic_url,
                    'organizer': activity.organizer,
                    'status': activity.status
                    }
            
            return {'view': 51, 'name': activity.name, 'description': activity.description,
                           'startTime': activity.start_time.isoformat()[:-6], 'endTime': activity.end_time.isoformat()[:-6],
                           'place': activity.place, 'picUrl': activity.pic_url, 'bgPicUrl': activity.bg_pic_url,
                           'organizer': activity.organizer, 'status': activity.status, 'acitivityid': nid}
        else:
            raise InputError()


class LotteryCreate(APIView):
    def get(self):
        print("Activity Create Get")
        if not self.request.user.is_authenticated():
            return {'view': 0}
        return {'view': 15}
    
    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        if 'create' in self.request.POST:
            self.check_input("name", "description", "first",
                            "second", "speical", 'third')
            Lottery.insertLottery(
                Activity.selectById(self.request.COOKIES['activityId']),
                self.input['name'],
                self.input['description'],
                self.input['first'],
                self.input['second'],
                self.input['third'],
                self.input['speical'],
                0
            )
            #obj = Lottery(name=self.input['name'],
                        #activity=Activity.selectById(self.input['activityId']),
                        #description=self.input['description'],
                        #first=self.input['first'],
                        #status=self.input['status'],
                        #second=self.input['second'],
                        #third=self.input['third'],
                        #speical=self.input['speical'],
                        #)
            #obj.save()

            #if not Lottery.objects.get(self.input['name']):
                #raise LogicError('lottery creat failed')
            #else:
            return {'view': 10}
            
        if 'return' in self.request.POST:
            return {'view': 10}


class LotteryDetail(APIView):
    def get(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        #self.check_input('id')
        #lottery = Lottery.objects.get(Lotter=self.input('id'))
        nid = self.request.GET.get('nid')
        lottery = Lottery.objects.filter(id=nid)
        lottery1 = lottery[0]

        #return data
        return {'view': 16, 'name': lottery1.name,
                           'description': lottery1.description,
                           'speical': lottery1.special,
                           'first': lottery1.first,
                           'second': lottery1.second,
                           'third': lottery1.third,
                           'status': lottery1.status}
                          
        #else:
            #raise InputError()

    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        if 'edit' in self.request.POST:
            self.check_input("name", "description", "first",
                         "second", "speical", 'third')
            nid = self.request.GET.get('nid')
            lottery = Lottery.objects.filter(id=nid)
            lottery1 = lottery[0]
            lottery1.updateLottery(
                lottery1.id,
                self.input['name'],
                self.input['description'],
                self.input['first'],
                self.input['second'],
                self.input['third'],
                self.input['speical'],
                lottery1.status
            )
            return {'view': 10}
        
        if 'return' in self.request.POST:
            return {'view': 10}
        
        if 'begin' in self.request.POST:
            nid = self.request.GET.get('nid')
            Lottery.objects.filter(id=nid).update(status=1)
            lottery = Lottery.objects.filter(id=nid)
            lottery1 = lottery[0]

            #return data
            return {'view': 16, 'name': lottery1.name,
                           'description': lottery1.description,
                           'speical': lottery1.special,
                           'first': lottery1.first,
                           'second': lottery1.second,
                           'third': lottery1.third,
                           'status': lottery1.status}
        
        if 'end' in self.request.POST:
            nid = self.request.GET.get('nid')
            Lottery.objects.filter(id=nid).update(status=2)
            lottery = Lottery.objects.filter(id=nid)
            lottery1 = lottery[0]

            #return data
            return {'view': 16, 'name': lottery1.name,
                           'description': lottery1.description,
                           'speical': lottery1.special,
                           'first': lottery1.first,
                           'second': lottery1.second,
                           'third': lottery1.third,
                           'status': lottery1.status}
        
        if 'detail' in self.request.POST:
            nid = self.request.GET.get('nid')
            Lottery.objects.filter(id=nid).delete()
            return {'view': 10}


class LotteryDelete(APIView):
    def get(self):
        nid = self.request.GET.get('nid')
        Lottery.objects.filter(id=nid).delete()
        return {'view': 10}


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
        #self.check_input('activityId')
        #lottery_list = Lottery.objects.filter(activity__id=self.input['activityId'])
        lottery_list = Lottery.selectByActivity(Activity.selectById(self.request.COOKIES['activityId']))
        #if not lottery_list:
            #raise InputError('no such activity')
        list = []
        for lottery in lottery_list:
            list.append({
                'name': lottery.name,
                'status': lottery.status,
                'id': lottery.id
            })
        ##return list
        #return render(APIView, 'a/lottery.html', {'list': list})
        return {'view': 19, 'list': list}
    
    def post(self):
        if 'activity' in self.request.POST:
            return {'view': 6}

        if 'barrage' in self.request.POST:
            return {'view': 9}

        if 'lottery' in self.request.POST:
            return {'view': 10}
        
        if 'create' in self.request.POST:
            #return redirect('/a/Lottery/create/')
            return {'view': 20}

        if 'logout' in self.request.POST:
            return {'view': 8}
        
        if 'return' in self.request.POST:
            return {'view': 27}
    
    
class ProgrameList(APIView):
    def get(self):
        #self.check_input('activityId')
        nid = self.request.GET.get('nid')
        if nid is not None:
            nid = self.request.GET.get('nid')
            #program_list = Programe.selectByActivity(Activity.selectById(self.input['activityId']))
            program_list = Programe.selectByActivity(Activity.selectById(nid))
            activityId = nid
        else:
            testtt = Activity.selectById(self.request.COOKIES['activityId'])
            program_list = Programe.selectByActivity(Activity.selectById(self.request.COOKIES['activityId']))
            activityId = self.request.COOKIES['activityId']
        show_list = []
        num = 0
        for program in program_list:
            num = num + 1
            show_list.append(
                {
                    'id' : program.id,
                    'name': program.name,
                    'sequence': program.sequence,
                    #'actor': program.actor
                }
            )
        n = len(show_list)
        for j in range(0, n - 1):
            for i in range(0, n - 1- j):
                if show_list[i]['sequence'] > show_list[i+1]['sequence']:
                    show_list[i], show_list[i+1] = show_list[i+1], show_list[i]
        return {'view': 25, 'list': show_list, 'activityId': activityId, 'num': num}
        
    def post(self):
        if 'activity' in self.request.POST:
            return {'view': 6}

        if 'barrage' in self.request.POST:
            return {'view': 9}

        if 'lottery' in self.request.POST:
            return {'view': 10}

        if 'logout' in self.request.POST:
            return {'view': 8}
        
        if 'return' in self.request.POST:
            return {'view': 27}

        if 'create' in self.request.POST:
            #return redirect('/a/Activity/create/')
            return {'view': 14}


class ProgrameDelete(APIView):
    def get(self):
        nid = self.request.GET.get('nid')
        Programe.objects.filter(id=nid).delete()
        #return redirect('/a/Activity/edit/')
        return {'view': 21}
    
    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        self.check_input('programId')
        Programe.deletePrograme(self.input['programId'])


class ProgrameCreate(APIView):
    def get(self):
        #nid = self.get().get('nid')
        #Programe.objects.filter(id=nid).delete()
        #return redirect('/a/Activity/edit/')
        return {'view': 22}

    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please Login First!")
        if 'create' in self.request.POST:
            self.check_input('name', 'description', 'actors')
            sequence = str(int(self.request.COOKIES['ProgrameNum']) + 1)
            Programe.insertPrograme(Activity.selectById(self.request.COOKIES['activityId']), self.input['name'],
                                    self.input['description'], sequence, self.input['actors'])
            '''if not Activity.objects.filter(self.input['name']):
                raise LogicError('fail creat pragram')
            else:
                return {'view': 6}'''
            
            return {'view': 6}
        
        if 'return' in self.request.POST:
            return {'view': 6}


class ProgrameDetail(APIView):
    def get(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        #self.check_input('programId')
        nid = self.request.GET.get('nid')
        programe = Programe.selectById(nid)
        if programe:
            data = {'name': programe.name,
                    'description': programe.description,
                    'sequence': programe.sequence,
                    'actors': programe.actors
                    }
            return {'view': 23, 'name': data['name'], 'description': data['description'], 'actors': data['actors']}
        else:
            raise InputError('no such programe')

    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        #self.check_input('programId')
        if 'edit' in self.request.POST:
            nid = self.request.GET.get('nid')
            programe = Programe.selectById(nid)
            old_programe = programe
            if programe:
                programe.updatePrograme(programe.id,
                                        self.input['name'],
                                        self.input['description'],
                                        self.input['actors'],
                                        programe.sequence)
            #else:
                #raise ValidateError('no such program')
            #programe.save()
            #if old_programe == programe:
                #return {'view': 21}
            #else:
                #return {'view': 21}
            return {'view': 21}
            
        if 'return' in self.request.POST:
                return {'view': 21}


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
        #self.check_input('activityId', 'commentId')
        show_list2 = []
        comment_list = Picture.objects.filter(activity=Activity.selectById(self.request.COOKIES['activityId']), status=1)
        #comment_list = Comment.objects.filter(time__lt=timezone.now().time.second).filter(id__gt=self.input['commentId'])
        for comment in comment_list:
            show_list2.append(
                {
                    'id': comment.id,
                    'picUrl': comment.pic_url
                }
            )
            
        show_list = []
        pic_list = Comment.objects.filter(activity=Activity.selectById(self.request.COOKIES['activityId']), status=1)
        #pic_list = Comment.objects.filter(time__lt=timezone.now().time.second ).filter(id__gt=self.input['pictureId'])
        for pic in pic_list:
            show_list.append(
                {
                    'id': pic.id,
                    'content': pic.content,
                    'color': pic.color,
                    'bolt': pic.bolt,
                    'incline': pic.incline,
                    'underline': pic.underline
                }
            )
        #return render(APIView, 'a/barrage.html', {'commentLinenumber': "", 'list': show_list, 'list2': show_list2})
        return {'view': 24, 'commentLinenumber': self.request.COOKIES['commentLinenumber'], 'list': show_list2, 'list2': show_list}
    
    def post(self):
        if 'activity' in self.request.POST:
            return {'view': 6}

        if 'barrage' in self.request.POST:
            return {'view': 9}

        if 'lottery' in self.request.POST:
            return {'view': 10}

        if 'logout' in self.request.POST:
            return {'view': 8}
        
        if 'return' in self.request.POST:
            return {'view': 27}
        
        if 'commentLinenumber' in self.request.POST:
            self.check_input('commentLinenumber')
            #self.request.COOKIES['commentLinenumber'] = self.input['ActivityID']
            #return self.input['commentLinenumber']
            show_list2 = []
            comment_list = Picture.objects.filter(activity=Activity.selectById(self.request.COOKIES['activityId']), status=1)
            #comment_list = Comment.objects.filter(time__lt=timezone.now().time.second).filter(id__gt=self.input['commentId'])
            for comment in comment_list:
                show_list2.append(
                    {
                        'id': comment.id,
                        'picUrl': comment.pic_url
                    }
                )
            
            show_list = []
            pic_list = Comment.objects.filter(activity=Activity.selectById(self.request.COOKIES['activityId']), status=1)
            #pic_list = Comment.objects.filter(time__lt=timezone.now().time.second ).filter(id__gt=self.input['pictureId'])
            for pic in pic_list:
                show_list.append(
                    {
                        'id': pic.id,
                        'content': pic.content,
                        'color': pic.color,
                        'bolt': pic.bolt,
                        'incline': pic.incline,
                        'underline': pic.underline
                    }
                )
            #return render(APIView, 'a/barrage.html', {'commentLinenumber': "", 'list': show_list, 'list2': show_list2})
            return {'view': 24, 'commentLinenumber': self.input['ActivityID'], 'list': show_list2, 'list2': show_list}
        
        if 'settop' in self.request.POST:
            self.check_input('content', 'color', 'bolt', 'incline', 'underline')
            Comment.objects.filter(status=3).delete()
            Comment.insertComment(Activity.selectById(self.request.COOKIES['activityId']), self.request.user, self.input['content'], self.input['color'],
                self.input['bolt'], self.input['underline'], self.input['incline'], timezone.now(), 3)
            show_list2 = []
            comment_list = Picture.objects.filter(activity=Activity.selectById(self.request.COOKIES['activityId']), status=1)
            #comment_list = Comment.objects.filter(time__lt=timezone.now().time.second).filter(id__gt=self.input['commentId'])
            for comment in comment_list:
                show_list2.append(
                    {
                        'id': comment.id,
                        'picUrl': comment.pic_url
                    }
                )
            
            show_list = []
            pic_list = Comment.objects.filter(activity=Activity.selectById(self.request.COOKIES['activityId']), status=1)
            #pic_list = Comment.objects.filter(time__lt=timezone.now().time.second ).filter(id__gt=self.input['pictureId'])
            for pic in pic_list:
                show_list.append(
                    {
                        'id': pic.id,
                        'content': pic.content,
                        'color': pic.color,
                        'bolt': pic.bolt,
                        'incline': pic.incline,
                        'underline': pic.underline
                    }
                )
            #return render(APIView, 'a/barrage.html', {'commentLinenumber': "", 'list': show_list, 'list2': show_list2})
            return {'view': 24, 'commentLinenumber': self.request.COOKIES['commentLinenumber'], 'list': show_list2, 'list2': show_list}
    
    
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
        self.check_input('id', 'status')
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


class barrage_left_detele(APIView):
    def get(self):
        nid = self.request.GET.get('nid')
        Picture.objects.filter(id=nid).delete()
        return {'view': 9}


class barrage_left_create(APIView):
    def get(self):
        return {'view': 9}


class barrage_right_detele(APIView):
    def get(self):
        nid = self.request.GET.get('nid')
        Comment.objects.filter(id=nid).delete()
        return {'view': 9}


class barrage_right_create(APIView):
    def get(self):
        return {'view': 9}


class ProgrameUp(APIView):
    def get(self):
        nid = self.request.GET.get('nid')
        programe = Programe.selectById(nid)
        num = str(int(programe.sequence) - 1)
        programe2 = Programe.objects.filter(activity=Activity.selectById(self.request.COOKIES['activityId']), sequence=num)
        if len(programe2) == 0:
            return {'view': 21}
        programe3 = programe2[0]
        if programe3:
            programe.updatePrograme(programe.id,
                                    programe.name,
                                    programe.description,
                                    programe.actors,
                                    programe3.sequence)
            programe.updatePrograme(programe3.id,
                                    programe3.name,
                                    programe3.description,
                                    programe3.actors,
                                    programe.sequence)
        return {'view': 21}

    
class ProgrameDown(APIView):
    def get(self):
        nid = self.request.GET.get('nid')
        programe = Programe.selectById(nid)
        num = str(int(programe.sequence) + 1)
        programe2 = Programe.objects.filter(activity=Activity.selectById(self.request.COOKIES['activityId']), sequence=num)
        if len(programe2) == 0:
            return {'view': 21}
        programe3 = programe2[0]
        if programe3:
            programe.updatePrograme(programe.id,
                                    programe.name,
                                    programe.description,
                                    programe.actors,
                                    programe3.sequence)
            programe.updatePrograme(programe3.id,
                                    programe3.name,
                                    programe3.description,
                                    programe3.actors,
                                    programe.sequence)
        return {'view': 21}
    
    
class Line(APIView):
    def get(self):
        return {'view': 50, 'number': self.request.COOKIES['commentLinenumber']}
    

class Top(APIView):
    def get(self):
        try:
            top = Comment.objects.get(status=3, activity=Activity.selectById(self.request.COOKIES['activityId']))
            show_list = []
            show_list.append(
                {
                    'content': top.content,
                    'bolt': top.bolt,
                    'incline': top.incline,
                    'color': top.color,
                    'underline': top.underline
                }
            )
            return {'view': 33, 'result': show_list}
        except:
            return {'view': 33, 'result': [{
                'content': '当前无置顶弹幕',
                'color': '16777215',
                'bolt': False,
                'incline': False,
                'underline': False}]}
        

class Pic(APIView):
    def get(self):
        pic_list = Picture.objects.filter(time__lt=timezone.now()+timedelta(seconds=-3), status=1, activity=Activity.selectById(self.request.COOKIES['activityId']))
        show_list = []
        for pic in pic_list:
            show_list.append(
                {
                    'picUrl': pic.pic_url.name
                }
            )
        pic_list = Picture.objects.filter(time__lt=timezone.now()+timedelta(seconds=-3), status=1, activity=Activity.selectById(self.request.COOKIES['activityId'])).delete()
        return {'view': 32, 'result': show_list}
    

class Barrier(APIView):
    def get(self):
        comment_list = Comment.objects.filter(time__lt=timezone.now()+timedelta(seconds=-3), status=1, activity=Activity.selectById(self.request.COOKIES['activityId']))
        #comment_list = Comment.objects.filter(time__lt=timezone.now() + timedelta(seconds=-3))
        result = []
        for i in comment_list:
            result.append({
                'content': i.content,
                'bolt': i.bolt,
                'color': i.color,
                'underline': i.underline,
                'incline': i.incline
            })
        Comment.objects.filter(time__lt=timezone.now() + timedelta(seconds=-3), status=1, activity=Activity.selectById(self.request.COOKIES['activityId'])).delete()
        return {'view': 31, 'result': result}
        
# Create your views here
