from django.shortcuts import render
from codex.baseerror import *
from codex.baseview import APIView
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.shortcuts import render, redirect

from DjangoProject import models
from DjangoProject.models import Activity, Lottery, Programe,Barrage,Comment,Picture
from django.utils import timezone
from wechat.views import CustomWeChatView
import uuid
from DjangoProject import settings
import os


class Login(APIView):
    def get(self):
        print("Login Get")
        if not self.request.user.is_authenticated():
            raise ValidateError("Please Login!")

    def post(self):
        if 'login' in self.post():
            self.check_input('username', 'password')
            user = authenticate(username=self.input['username'], password=self.input['password'])
            if user is not None and user.is_active:
                login(self.request, user)
                return redirect('/a/activity/')
            if not User.objects.filter(username=self.input['username']):
                raise ValidateError("Username not exist")

            raise ValidateError("wrong password")
        
        else:
            return redirect('/a/register/')


class Register(APIView):
    def post(self):
        if 'register' in self.post():
            self.check_input('username', 'password')
            if User.objects.get(username=self.input['username']):
                raise ValidateError('The username has been occupied')
            else:
                user = User.objects.create_user(username=self.input['username'], password=self.input['password'],
                                                email='example@163.com')
                user.save()
            if not User.objects.get(self.input['username']):
                raise ValidateError('register failed')
            else:
                return render(APIView, 'a/register.html', {
                    'username': self.input['username'],
                    'password': self.input['password'],
                    'status': 'registration success'
                })
            
        else:
            return redirect('/a/login/')


class Logout(APIView):

    def get(self):
        print("Log out Post")
        if not self.request.user.is_authenticated():
            raise LogicError('no user is online')
        else:
            logout(self.request)
        return redirect('/a/login/')


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
                'place': i.place,
            })
        return render(APIView, 'a/activity.html', {'list': output_list})
    
    def post(self):
        if 'activity' in self.post():
            return redirect('/a/activity/')

        if 'barrage' in self.post():
            return redirect('/a/barrage/')

        if 'lottery' in self.post():
            return redirect('/a/lottery/')

        if 'create' in self.post():
            return redirect('/a/Activity/create/')

        if 'logout' in self.post():
            return redirect('/a/logout/')


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
        nid = self.get().get('nid')
        Activity.objects.filter(activityId=nid)
        return redirect('/a/activity/')


class ActivityCreate(APIView):

    def post(self):

        if not self.request.user.is_authenticated():
            raise ValidateError("Please Login First!")
        if 'create' in self.post():
            self.check_input("name", "place", "description", "picUrl", "bgPicUrl", "startTime",
                             "endTime", "status", "organizer")
            Activity.insertActivity(self.input['organizer'], self.input['description'], self.input['picUrl'],
                                    self.input['startTime'], self.input['endTime'],
                                    self.input['bgPicUrl'], self.input['status'], self.input['palce'], self.input['name'])
            if not Activity.objects.get(self.input['name']):
                raise LogicError()
            else:
                return redirect('/a/activity/')
            
        if 'return' in self.post():
            return redirect('/a/activity/')


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
        nid = self.get().get('nid')
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

            #return data
            program_list = Programe.selectByActivity(Activity.selectById(self.input['activityId']))
            show_list = []
            for program in program_list:
                show_list.append(
                    {
                        'name': program.name,
                        'sequence': program.sequence,
                        'actor': program.actor,
                        'id': program.id
                    }
                )
            
            return render(APIView, 'a/Activity/edit.html',
                          {'Name': Activity.name, 'description': Activity.description,
                           'startTime': Activity.start_timeime.timestamp(), 'endTime': Activity.end_time.timestamp(),
                           'place': activity.place, 'picUrl': activity.pic_url, 'bgPicUrl': activity.bg_pic_url,
                           'organizer': activity.organizer, 'status': activity.status, 'list': show_list})
        else:
            raise InputError()

    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        
        if 'edit' in self.post():
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
            # return 0
            return redirect('/a/activity/')
        
        if 'create' in self.post():
            return redirect('/a/Programe/create/')
        
        if 'return' in self.post():
            return redirect('/a/activity/')
        
        if 'begin' in self.post():
            Activity.updateActivity(self.input['activityId'],self.input['organizer'], self.input['description'],
                                            self.input['picUrl'],
                                            self.input['startTime'], self.input['endTime'],
                                            self.input['bgPicUrl'], 1, self.input['palce'],
                                            self.input['name'])
            return render(APIView, 'a/Activity/edit.html')
        
        if 'end' in self.post():
            Activity.updateActivity(self.input['activityId'],self.input['organizer'], self.input['description'],
                                            self.input['picUrl'],
                                            self.input['startTime'], self.input['endTime'],
                                            self.input['bgPicUrl'], 2, self.input['palce'],
                                            self.input['name'])
            return render(APIView, 'a/Activity/edit.html')
        
        if 'detail' in self.post():
            nid = self.get().get('nid')
            Activity.objects.filter(activityId=nid)
            return redirect('/a/activity/')


class LotteryCreate(APIView):
    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        if 'create' in self.post():
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
            else:
                return redirect('/a/lottery/')
            
        if 'return' in self.post():
            return redirect('/a/lottery/')


class LotteryDetail(APIView):
    def get(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        #self.check_input('id')
        #lottery = Lottery.objects.get(Lotter=self.input('id'))
        nid = APIView.get().get('nid')
        lottery = Lottery.objects.get(id=nid)
        if lottery:
            data = {'name': lottery.name,
                    'description': lottery.description,
                    'speical': lottery.special,
                    'first': lottery.first,
                    'second': lottery.second,
                    'third': lottery.third,
                    'status': lottery.status
                    }

            #return data
            return render(APIView, 'a/Lottery/edit.html',
                          {'name': lottery.name,
                           'description': lottery.description,
                           'speical': lottery.special,
                           'first': lottery.first,
                           'second': lottery.second,
                           'third': lottery.third,
                           'status': lottery.status})
                          
        else:
            raise InputError()

    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        if 'edit' in self.post():
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
            return redirect('/a/lottery/')
        
        if 'return' in self.post():
            return redirect('/a/lottery/')
        
        if 'begin' in self.post():
            nid = self.get().get('nid')
            Lottery.objects.filter(id=nid).update(Statue="1")
            return render(APIView, 'a/Lottery/edit.html')
        
        if 'end' in self.post():
            nid = self.get().get('nid')
            Lottery.objects.filter(id=nid).update(Statue="2")
            return render(APIView, 'a/Lottery/edit.html')
        
        if 'detail' in self.post():
            nid = self.get().get('nid')
            Lottery.objects.filter(id=nid).delete()
            return redirect('/a/lottery/')


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
                'name': lottery.name,
                'status': lottery.status,
                'id': lottery.id
            })
        ##return list
        return render(APIView, 'a/lottery.html', {'list': list})
    
    def post(self):
        if 'activity' in self.post():
            return redirect('/a/activity/')

        if 'barrage' in self.post():
            return redirect('/a/barrage/')

        if 'lottery' in self.post():
            return redirect('/a/lottery/')

        if 'create' in self.post():
            return redirect('/a/Lottery/create/')

        if 'edit' in self.post():
            return redirect('/a/Lottery/edit/')

        if 'logout' in self.post():
            return redirect('/a/logout/')
    
    
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
    def get(self):
        nid = self.get().get('nid')
        Programe.objects.filter(id=nid).delete()
        return redirect('/a/Activity/edit/')
    
    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        self.check_input('programId')
        Programe.deletePrograme(self.input['programId'])


class ProgrameCreate(APIView):

    def post(self):

        if not self.request.user.is_authenticated():
            raise ValidateError("Please Login First!")
        if 'create' in self.post():
            self.check_input('activityId', 'name', 'description', 'sequence', 'actors')
            Programe.insertPrograme(Activity.selectById(self.input['activityId']), self.input['name'],
                                    self.input['description'], self.input['sequence'], self.input['actors'])
            if not Activity.objects.get(self.input['name']):
                raise LogicError('fail creat pragram')
            else:
                return redirect('/a/Activity/edit/')
            
        if 'retrun' in self.post():
            return redirect('/a/Activity/edit/')


class ProgrameDetail(APIView):
    def get(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        #self.check_input('programId')
        nid = self.get().get('nid')
        programe = Programe.selectById(nid)
        if programe:
            data = {'name': programe.name,
                    'description': programe.description,
                    'sequence': programe.sequence,
                    'actors': programe.actors
                    }
            return render(APIView, 'a/Programe/edit.html',
                          {'name': programe.name, 'description': programe.description, 'sequence': programe.sequence, 'actors': programe.actors})
        else:
            raise InputError('no such programe')

    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        #self.check_input('programId')
        if 'edit' in self.post():
            nid = self.get().get('nid')
            programe = Programe.selectById[nid]
            old_programe = programe
            if programe:
                programe.updatePrograme(#self.input['programId'],
                                        self.input['name'],
                                        self.input['description']
                                        , self.input['actors'], self.input['sequence'])
            else:
                raise ValidateError('no such program')
            programe.save()
            if old_programe == programe:
                raise InputError('no change!')
            else:
                return redirect('/a/Activity/edit/')
            
        if 'return' in self.post():
            return redirect('/a/Activity/edit/')


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
        self.check_input('activityId', 'commentId')
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
            
        show_list2 = []
        pic_list = Comment.objects.filter(time__lt=timezone.now().time.second ).filter(id__gt=self.input['pictureId'])
        for pic in pic_list:
            show_list2.append(
                {
                    'id': pic.id,
                    'picUrl': pic.pic_url
                }
            )
        return render(APIView, 'a/barrage.html', {'commentLinenumber': "", 'list': show_list, 'list2': show_list2})
    
    def post(self):
        if 'activity' in self.post():
            return redirect('/a/activity/')

        if 'barrage' in self.post():
            return redirect('/a/barrage/')

        if 'lottery' in self.post():
            return redirect('/a/lottery/')

        if 'logout' in self.post():
            return redirect('/a/logout/')
        
        if 'commentLinenumber' in self.post():
            self.check_input('commentLinenumber')
            return self.input['commentLinenumber']
        
        if 'settop' in self.post():
            self.check_input('content', 'color', 'bolt', 'incline', 'underline')
            old_top = Comment.objects.get(status=Barrage.TOP)
            old_top.status = Barrage.NOT_OK
            old_top.save()
            Comment.insertComment(Activity.selectById(self.input['activityId']),self.request.user.username,self.input['color'],self.input['content'],
                self.input['bolt'], self.input['underline'] ,self.input['incline'],timezone.now(),Barrage.TOP)
    
    
#这个get我在setcomment的那个class里面就直接同时两个一起加载了
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
        nid = self.GET.get('nid')
        Barrage.objects.filter(id=nid).delete()
        return redirect('/a/barrage/')


#左右两个添加不知道怎么实现，就是审核可以放到弹幕墙上面的弹幕
class barrage_left_create(APIView):
    def get(self):


class barrage_right_detele(APIView):
    def get(self):
        nid = self.GET.get('nid')
        Barrage.objects.filter(id=nid).delete()
        return redirect('/a/barrage/')


class barrage_right_create(APIView):
    def get(self):


# 实现一下点击节目顺序往上
class ProgrameUp(APIView):


# 实现一下点击节目顺序往下
class ProgrameDown(APIView):

# Create your views here.
