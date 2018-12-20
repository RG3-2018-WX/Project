from django.shortcuts import render
from codex.baseerror import *
from codex.baseview import APIView
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User

from DjangoProject import models
from DjangoProject.models import Activity, Lottery, Programe, Barrage, Comment, Picture
from django.utils import timezone
from wechat.views import CustomWeChatView
import uuid
from DjangoProject import settings
import os

activityid = 0


class Login(APIView):
    def get(self):
        print("Login Get")
        if not self.request.user.is_authenticated():
            #raise ValidateError("Please Login!")
            return {'view': 0}

        return {'view': 0}

    def post(self):
        if 'login' in self.request.POST:
            self.check_input('username', 'password')
            user = authenticate(username=self.input['username'], password=self.input['password'])
            if user is not None and user.is_active:
                login(self.request, user)
                return {'view': 6}
            if not User.objects.filter(username=self.input['username']):
                #raise ValidateError("Username not exist")
                return {'view': 2, 'msg': 'Username not exist'}

            #raise ValidateError("wrong password")
            return {'view': 2, 'msg': 'wrong password'}
        
        if 'register' in self.request.POST:
            return {'view': 1}


class Register(APIView):
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
            return {'view': 4}


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
        return {'view': 7, 'msg': output_list}
    
    def post(self):
        if 'activity' in self.request.POST:
            #return redirect('/a/activity/')
            return {'view': 6}

        if 'barrage' in self.request.POST:
            #return redirect('/a/barrage/')
            return {'view': 9}

        if 'lottery' in self.request.POST:
            #return redirect('/a/lottery/')
            return {'view': 10}

        if 'create' in self.request.POST:
            #return redirect('/a/Activity/create/')
            return {'view': 11}

        if 'logout' in self.request.POST:
            return {'view': 8}


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
        return {'view': 6}


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
                             "endTime", "status", "organizer")
            Activity.insertActivity(self.input['organizer'], self.input['description'], self.input['picUrl'],
                                    self.input['startTime'], self.input['endTime'],
                                    self.input['bgPicUrl'], self.input['status'], self.input['palce'], self.input['name'])
            if not Activity.objects.get(self.input['name']):
                raise LogicError()
            else:
                return {'view': 6}
            
        if 'return' in self.request.POST:
            return {'view': 6}


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
            
            return {'view': 13, 'Name': Activity.name, 'description': Activity.description,
                           'startTime': Activity.start_timeime.timestamp(), 'endTime': Activity.end_time.timestamp(),
                           'place': activity.place, 'picUrl': activity.pic_url, 'bgPicUrl': activity.bg_pic_url,
                           'organizer': activity.organizer, 'status': activity.status}
        else:
            raise InputError()

    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        
        if 'edit' in self.request.POST:
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
            return {'view': 6}
        
        if 'return' in self.request.POST:
            return {'view': 6}
        
        if 'begin' in self.request.POST:
            Activity.updateActivity(self.input['activityId'],self.input['organizer'], self.input['description'],
                                            self.input['picUrl'],
                                            self.input['startTime'], self.input['endTime'],
                                            self.input['bgPicUrl'], 1, self.input['palce'],
                                            self.input['name'])
            return {'view': 18}
        
        if 'end' in self.request.POST:
            Activity.updateActivity(self.input['activityId'],self.input['organizer'], self.input['description'],
                                            self.input['picUrl'],
                                            self.input['startTime'], self.input['endTime'],
                                            self.input['bgPicUrl'], 2, self.input['palce'],
                                            self.input['name'])
            return {'view': 18}
        
        if 'detail' in self.request.POST:
            nid = self.get().get('nid')
            Activity.objects.filter(activityId=nid)
            return {'view': 6}


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
                return {'view': 10}
            
        if 'return' in self.request.POST:
            return {'view': 10}


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
            return {'view': 16, 'name': lottery.name,
                           'description': lottery.description,
                           'speical': lottery.special,
                           'first': lottery.first,
                           'second': lottery.second,
                           'third': lottery.third,
                           'status': lottery.status}
                          
        else:
            raise InputError()

    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        if 'edit' in self.request.POST:
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
            return {'view': 10}
        
        if 'return' in self.request.POST:
            return {'view': 10}
        
        if 'begin' in self.request.POST:
            nid = self.get().get('nid')
            Lottery.objects.filter(id=nid).update(Statue="1")
            return {'view': 17}
        
        if 'end' in self.request.POST:
            nid = self.get().get('nid')
            Lottery.objects.filter(id=nid).update(Statue="2")
            return {'view': 17}
        
        if 'detail' in self.request.POST:
            nid = self.get().get('nid')
            Lottery.objects.filter(id=nid).delete()
            return {'view': 10}


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
        #self.check_input('activityId')
        #lottery_list = Lottery.objects.filter(activity__id=self.input['activityId'])
        lottery_list = Lottery.objects.filter(activityid)
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
    
    
class ProgrameList(APIView):
    def get(self):
        #self.check_input('activityId')
        nid = self.request.GET.get('nid')
        if nid is not None:
            activityid = nid
        #program_list = Programe.selectByActivity(Activity.selectById(self.input['activityId']))
        program_list = Programe.selectByActivity(Activity.selectById(activityid))
        show_list = []
        for program in program_list:
            show_list.append(
                {
                    'name': program.name,
                    'sequence': program.sequence,
                    'actor': program.actor
                }
            )
        show_list = []
        return {'view': 25, 'list': show_list}
        
    def post(self):
        if 'activity' in self.request.POST:
            return {'view': 6}

        if 'barrage' in self.request.POST:
            return {'view': 9}

        if 'lottery' in self.request.POST:
            return {'view': 10}

        if 'logout' in self.request.POST:
            return {'view': 8}

        if 'create' in self.request.POST:
            #return redirect('/a/Activity/create/')
            return {'view': 14}


class ProgrameDelete(APIView):
    def get(self):
        nid = self.get().get('nid')
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
            self.check_input('activityId', 'name', 'description', 'sequence', 'actors')
            Programe.insertPrograme(Activity.selectById(self.input['activityId']), self.input['name'],
                                    self.input['description'], self.input['sequence'], self.input['actors'])
            if not Activity.objects.get(self.input['name']):
                raise LogicError('fail creat pragram')
            else:
                return {'view': 6}
             
        if 'return' in self.request.POST:
            return {'view': 6}


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
            return {'view': 23, 'name': programe.name, 'description': programe.description, 'sequence': programe.sequence, 'actors': programe.actors}
        else:
            raise InputError('no such programe')

    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        #self.check_input('programId')
        if 'edit' in self.request.POST:
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
        show_list=[]
        #comment_list = Comment.objects.filter(time__lt=timezone.now().time.second).filter(id__gt=self.input['commentId'])
        #for comment in comment_list:
            #show_list.append(
                #{
                    #'id': comment.id,
                    #'content': comment.content,
                    #'color': comment.color,
                    #'bolt': comment.bolt,
                    #'incline': comment.incline,
                    #'underline': comment.underline
                #}
            #)
            
        show_list2 = []
        #pic_list = Comment.objects.filter(time__lt=timezone.now().time.second ).filter(id__gt=self.input['pictureId'])
        #for pic in pic_list:
            #show_list2.append(
                #{
                    #'id': pic.id,
                    #'picUrl': pic.pic_url
                #}
            #)
        #return render(APIView, 'a/barrage.html', {'commentLinenumber': "", 'list': show_list, 'list2': show_list2})
        return {'view': 24, 'commentLinenumber': "", 'list': show_list, 'list2': show_list2}
    
    def post(self):
        if 'activity' in self.request.POST:
            return {'view': 6}

        if 'barrage' in self.request.POST:
            return {'view': 9}

        if 'lottery' in self.request.POST:
            return {'view': 10}

        if 'logout' in self.request.POST:
            return {'view': 8}
        
        if 'commentLinenumber' in self.request.POST:
            self.check_input('commentLinenumber')
            return self.input['commentLinenumber']
        
        if 'settop' in self.request.POST:
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
        return {'view': 9}


#左右两个添加不知道怎么实现，就是审核可以放到弹幕墙上面的弹幕
class barrage_left_create(APIView):
    def get(self):
        return {'view': 9}



class barrage_right_detele(APIView):
    def get(self):
        nid = self.GET.get('nid')
        Barrage.objects.filter(id=nid).delete()
        return {'view': 9}


class barrage_right_create(APIView):
    def get(self):
        return {'view': 9}


# 实现一下点击节目顺序往上
class ProgrameUp(APIView):
    def get(self):
        return {'view': 21}

    

# 实现一下点击节目顺序往下
class ProgrameDown(APIView):
    def get(self):
        return {'view': 21}


# Create your views here