# -*- coding: utf-8 -*-
#
import json
import logging

from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import JsonResponse
from codex.baseerror import BaseError, InputError


__author__ = "Epsirom"


class BaseView(View):

    logger = logging.getLogger('View')

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return self.do_dispatch(*args, **kwargs)

    def do_dispatch(self, *args, **kwargs):
        raise NotImplementedError('You should implement do_dispatch() in sub-class of BaseView')

    def http_method_not_allowed(self, *args, **kwargs):
        return super(BaseView, self).http_method_not_allowed(self.request, *args, **kwargs)


class APIView(BaseView):

    logger = logging.getLogger('API')

    def do_dispatch(self, *args, **kwargs):
        self.input = self.query or self.body
        handler = getattr(self, self.request.method.lower(), None)
        if not callable(handler):
            return self.http_method_not_allowed()
        return self.api_wrapper(handler, *args, **kwargs)

    @property
    def body(self):
        return json.loads(self.request.body.decode() or '{}')

    @property
    def query(self):
        d = getattr(self.request, self.request.method, None)
        if d:
            d = d.dict()
        else:
            d = dict()
        d.update(self.request.FILES)
        return d

    def api_wrapper(self, func, *args, **kwargs):
        code = 0
        msg = ''
        result = None
        try:
            result = func(*args, **kwargs)
        except BaseError as e:
            code = e.code
            msg = e.msg
            self.logger.exception('Error occurred when requesting %s: %s', self.request.path, e)
        except Exception as e:
            code = -1
            msg = str(e)
            self.logger.exception('Error occurred when requesting %s: %s', self.request.path, e)
        try:
            response = {
                'code': code,
                'msg': msg,
                'data': result,
            }
        except:
            self.logger.exception('JSON Serializing failed in requesting %s', self.request.path)
            code = -1
            msg = 'Internal Error'
            response = {
                'code': code,
                'msg': msg,
                'data': None,
            }
            
        #登入页面
        if result is None:
            return JsonResponse(response)
        if 'view' in result:
            if result['view'] == 26:
                return render(self.request, 'a/login.html')
            if result['view'] == 1:
                return redirect('/a/register/')
            if result['view'] == 2:
                return render(self.request, 'a/login.html', {'username': result['username'], 'password': result['password']})
            if result['view'] == 27:
                return redirect('/a/activity/')
            if result['view'] == 0:
                return redirect('/')
        
            #注册页面
            if result['view'] == 3:
                return render(self.request, 'a/register.html')
            if result['view'] == 4:
                return redirect('/')
            if result['view'] == 5:
                return render(self.request, 'a/register.html', {'status': result['msg']})
        
            #活动界面
            if result['view'] == 6:
                return redirect('/a/programe/')
            if result['view'] == 7:
                return render(self.request, 'a/activity.html', {'list': result['msg']})
            if result['view'] == 8:
                return redirect('/a/logout/')
            if result['view'] == 9:
                return redirect('/a/barrage/')
            if result['view'] == 10:
                return redirect('/a/lottery/')
            if result['view'] == 11:
                return redirect('/a/Activity/create/')
            if result['view'] == 12:
                return render(self.request, 'a/Activity/create.html')
            if result['view'] == 13:
                return render(self.request, 'a/Activity/edit.html', {'name': result['name'], 'description': result['description'],
                           'startTime': result['startTime'], 'endTime': result['endTime'],
                           'place': result['place'], 'picUrl': result['picUrl'], 'bgPicUrl': result['bgPicUrl'],
                           'status': result['status'], 'id': result['acitivityid']})
            if result['view'] == 18:
                return render(self.request, 'a/Activity/edit.html')
        
            #节目界面
            if result['view'] == 25:
                r = render(self.request, 'a/programe.html', {'list': result['list']})
                r.set_cookie('activityId', result['activityId'])
                r.set_cookie('commentLinenumber', 5)
                r.set_cookie('ProgrameNum', result['num'])
                return r
            if result['view'] == 14:
                return redirect('/a/Programe/create/')
            if result['view'] == 21:
                return redirect('/a/programe/')
            if result['view'] == 22:
                return render(self.request, 'a/Programe/create.html')
            if result['view'] == 23:
                return render(self.request, 'a/Programe/edit.html', {'name': result['name'], 'description': result['description'], 'actors': result['actors']})
        
        
            #抽奖界面
            if result['view'] == 15:
                return render(self.request, 'a/Lottery/create.html')
            if result['view'] == 16:
                return render(self.request, 'a/Lottery/edit.html',{'name': result['name'],
                           'description': result['description'],
                           'speical': result['speical'],
                           'first': result['first'],
                           'second': result['second'],
                           'third': result['third'],
                           'status': result['status']})
            if result['view'] == 17:
                return render(self.request, 'a/Lottery/edit.html')
            if result['view'] == 19:
                return render(self.request, 'a/lottery.html', {'list': result['list']})
            if result['view'] == 20:
                return redirect('/a/Lottery/create/')
        
            #弹幕页面
            if result['view'] == 24:
                r = render(self.request, 'a/barrage.html', {'commentLinenumber': result['commentLinenumber'], 'list': result['list'], 'list2': result['list2']})
                r.set_cookie('commentLinenumber', result['commentLinenumber'])
                return r
                #return render(self.request, 'a/barrage.html', {'commentLinenumber': result['commentLinenumber'], 'list': result['list'], 'list2': result['list2']})
        
            #弹幕墙页面
            if result['view'] == 30:
                return render(self.request, 'b/2.html', {'value': result['r']})
                #return JsonResponse({'con': "",
                        #'picurl' : "",
                        #'color' : "",
                        #'bolt' : "",
                        #'incline' : "",
                        #'underline': ""})
        
            if result['view'] == 31:
                return JsonResponse(result['result'], safe=False)
        
            if result['view'] == 32:
                return JsonResponse(result['result'], safe=False)
        
            if result['view'] == 33:
                return JsonResponse(result['result'], safe=False)
        
            if result['view'] == 40:
                return JsonResponse(response)
        
            if result['view'] == 41:
                return JsonResponse(response)
        
            if result['view'] == 42:
                J = JsonResponse(response)
                J.set_cookie('sequence', result['sequence'])
                return J
        
            if result['view'] == 55:
                return render(self.request, 'b/2.html')
        
            if result['view'] == 50:
                return JsonResponse({'linenumber': int(result['number'])})
            
            if result['view'] == 51:
                return render(self.request, 'a/Activitys.html', {'name': result['name'], 'description': result['description'],
                           'startTime': result['startTime'], 'endTime': result['endTime'],
                           'place': result['place'], 'picUrl': result['picUrl'], 'bgPicUrl': result['bgPicUrl'],
                           'status': result['status'], 'id': result['acitivityid']})

        return JsonResponse(response, content_type="application/json",safe=False)

    def check_input(self, *keys):
        for k in keys:
            if k not in self.input:
                raise InputError('Field "%s" required' % (k, ))
