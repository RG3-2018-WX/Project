from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Lottery, Barrage, Activity, Barrage2


def llogin(request):
    if request.method == 'GET':
        return render(request, 'a/login.html')

    if request.method == 'POST':
        if 'login' in request.POST:
            input_username = request.POST['username']
            input_password = request.POST['password']

            user = authenticate(username=input_username, password=input_password)

            if user is not None:
                login(request, user)
                return redirect('/a/activity/')
            else:
                return render(request, 'a/login.html', {
                    'username': input_username,
                    'password': input_password,
                    'status': 'ERROR Incorrect username or password'
                })

        if 'register' in request.POST:
            return redirect('/a/register/')

    return render(request, 'a/login.html')


def Logout(request):
    if request.method == 'GET':
        logout(request)
        return redirect('/a/login/')

    if request.method == 'POST':
        return redirect('/a/login/')


def register(request):
    if request.method == 'GET':
        return render(request, 'a/register.html')

    if request.method == 'POST':
        if 'register' in request.POST:
            input_username = request.POST['username']
            input_password = request.POST['password']

            user = User.objects.create_user(username=input_username, password=input_password)

            if user is False:
                return render(request, 'a/register.html', {
                    'username': input_username,
                    'password': input_password,
                    'status': 'registration failed',
                })
            else:
                return render(request, 'a/register.html', {
                    'username': input_username,
                    'password': input_password,
                    'status': 'registration success'
                })

        if 'return' in request.POST:
            return redirect('/a/login/')

    return render(request, 'a/register.html')


def activity(request):
    if request.method == 'GET':
        if not request.user.is_authenticated():
            return redirect('/a/login/')
        else:
            lists = Activity.objects.all()
            print(lists)
            return render(request, 'a/activity.html', {'list': lists})

    if request.method == 'POST':
        if 'activity' in request.POST:
            return redirect('/a/activity/')

        if 'barrage' in request.POST:
            return redirect('/a/barrage/')

        if 'lottery' in request.POST:
            return redirect('/a/lottery/')

        if 'create' in request.POST:
            return redirect('/a/Activity/create/')

        if 'edit' in request.POST:
            return redirect('/a/Activity/edit/')

        if 'logout' in request.POST:
            return redirect('/a/logout/')

    return render(request, 'a/activity.html')


def barrage(request):
    if request.method == 'GET':
        if not request.user.is_authenticated():
            return redirect('/a/login/')
        else:
            lists = Barrage.objects.all()
            lists2 = Barrage2.objects.all()
            print(lists)
            return render(request, 'a/barrage.html', {'list': lists, 'list2':lists2})

    if request.method == 'POST':
        if 'activity' in request.POST:
            return redirect('/a/activity/')

        if 'barrage' in request.POST:
            return redirect('/a/barrage/')

        if 'lottery' in request.POST:
            return redirect('/a/lottery/')

        if 'logout' in request.POST:
            return redirect('/a/logout/')

    return render(request, 'a/barrage.html')


def lottery(request):
    if request.method == 'GET':
        if not request.user.is_authenticated():
            return redirect('/a/login/')
        else:
            lists = Lottery.objects.all()
            print(lists)
            return render(request, 'a/lottery.html', {'list': lists})

    if request.method == 'POST':
        if 'activity' in request.POST:
            return redirect('/a/activity/')

        if 'barrage' in request.POST:
            return redirect('/a/barrage/')

        if 'lottery' in request.POST:
            return redirect('/a/lottery/')

        if 'create' in request.POST:
            return redirect('/a/Lottery/create/')

        if 'edit' in request.POST:
            return redirect('/a/Lottery/edit/')

        if 'logout' in request.POST:
            return redirect('/a/logout/')

    return render(request, 'a/lottery.html')


def activity_create(request):
    if request.method == 'GET':
        if not request.user.is_authenticated():
            return redirect('/a/login/')
        else:
            return render(request, 'a/Activity/create.html',
                          {'ActivityID': "0", 'Name': "1", 'Organnizer': "1", 'Description': "1"})

    if request.method == 'POST':
        if 'create' in request.POST:
            ActivityID = request.POST['ActivityID']
            Name = request.POST['Name']
            Organnizer = request.POST['Organnizer']
            Description = request.POST['Description']
            Activity.objects.create(ActivityID=ActivityID, Name=Name, Organnizer=Organnizer, Description=Description, StartTime="00:00", EndTime="00:00", Statue="未开始")
            return redirect('/a/activity/')

        if 'return' in request.POST:
            return redirect('/a/activity/')

        return render(request, 'a/Activity/create.html')


def activity_edit(request):
    nid = request.GET.get('nid')
    if request.method == 'GET':
        if not request.user.is_authenticated():
            return redirect('/a/login/')
        else:
            obj = Activity.objects.get(id=nid)
            ActivityID = obj.ActivityID
            Name = obj.Name
            Organnizer = obj.Organnizer
            Description = obj.Description
            Statue = obj.Statue
            return render(request, 'a/Activity/edit.html',
                          {'ActivityID': ActivityID, 'Name': Name, 'Organnizer': Organnizer, 'Description': Description, 'Statue': Statue})

    if request.method == 'POST':
        if 'edit' in request.POST:
            Activity.objects.filter(id=nid).update(ActivityID=request.POST['ActivityID'])
            Activity.objects.filter(id=nid).update(Name=request.POST['Name'])
            Activity.objects.filter(id=nid).update(Organnizer=request.POST['Organnizer'])
            Activity.objects.filter(id=nid).update(Description=request.POST['Description'])
            return redirect('/a/activity/')

        if 'return' in request.POST:
            return redirect('/a/activity/')

        if 'begin' in request.POST:
            Activity.objects.filter(id=nid).update(Statue="进行中")
            obj = Activity.objects.get(id=nid)
            ActivityID = obj.ActivityID
            Name = obj.Name
            Organnizer = obj.Organnizer
            Description = obj.Description
            Statue = obj.Statue
            return render(request, 'a/Activity/edit.html',
                          {'ActivityID': ActivityID, 'Name': Name, 'Organnizer': Organnizer, 'Description': Description, 'Statue': Statue})

        if 'end' in request.POST:
            Activity.objects.filter(id=nid).update(Statue="结束")
            obj = Activity.objects.get(id=nid)
            ActivityID = obj.ActivityID
            Name = obj.Name
            Organnizer = obj.Organnizer
            Description = obj.Description
            Statue = obj.Statue
            return render(request, 'a/Activity/edit.html',
                          {'ActivityID': ActivityID, 'Name': Name, 'Organnizer': Organnizer, 'Description': Description, 'Statue': Statue})

        if 'detail' in request.POST:
            Activity.objects.filter(id=nid).delete()
            return redirect('/a/activity/')

        return render(request, 'a/Activity/edit.html')


def activity_up(request):
    if request.method == 'GET':
        if not request.user.is_authenticated():
            return redirect('/a/login/')

        return render(request, 'a/Activity/up.html')

    if request.method == 'POST':
        return render(request, 'a/Activity/up.html')


def activity_down(request):
    if request.method == 'GET':
        if not request.user.is_authenticated():
            return redirect('/a/login/')

        return render(request, 'a/Activity/down.html')

    if request.method == 'POST':
        return render(request, 'a/Activity/down.html')


def lottery_create(request):
    if request.method == 'GET':
        if not request.user.is_authenticated():
            return redirect('/a/login/')
        else:
            return render(request, 'a/Lottery/create.html',
                          {'ActivityID': "0", 'IDs': "0", 'Name': "", 'Description': "", 'First': "0", 'Second': "0",
                           'Third': "0", 'Special': "0"})

    if request.method == 'POST':
        if 'create' in request.POST:
            ActivityID = request.POST['ActivityID']
            IDs = request.POST['IDs']
            Name = request.POST['Name']
            Description = request.POST['Description']
            First = request.POST['First']
            Second = request.POST['Second']
            Third = request.POST['Third']
            Special = request.POST['Special']
            Lottery.objects.create(ActivityID=ActivityID, IDs=IDs, Name=Name, Description=Description, First=First,
                                   Second=Second, Third=Third, Special=Special, Statue="未开始")
            return redirect('/a/lottery/')

        if 'return' in request.POST:
            return redirect('/a/lottery/')


def lottery_edit(request):
    nid = request.GET.get('nid')
    if request.method == 'GET':
        if not request.user.is_authenticated():
            return redirect('/a/login/')
        else:
            obj = Lottery.objects.get(id=nid)
            ActivityID = obj.ActivityID
            IDs = obj.IDs
            Name = obj.Name
            Description = obj.Description
            First = obj.First
            Second = obj.Second
            Third = obj.Third
            Special = obj.Special
            Statue = obj.Statue
            return render(request, 'a/Lottery/edit.html',
                          {'ActivityID': ActivityID, 'IDs': IDs, 'Name': Name, 'Description': Description,
                           'First': First, 'Second': Second, 'Third': Third, 'Special': Special, 'Statue': Statue})

    if request.method == 'POST':
        if 'edit' in request.POST:
            Lottery.objects.filter(id=nid).update(ActivityID=request.POST['ActivityID'])
            Lottery.objects.filter(id=nid).update(IDs=request.POST['IDs'])
            Lottery.objects.filter(id=nid).update(Name=request.POST['Name'])
            Lottery.objects.filter(id=nid).update(Description=request.POST['Description'])
            Lottery.objects.filter(id=nid).update(First=request.POST['First'])
            Lottery.objects.filter(id=nid).update(Second=request.POST['Second'])
            Lottery.objects.filter(id=nid).update(Third=request.POST['Third'])
            Lottery.objects.filter(id=nid).update(Special=request.POST['Special'])
            return redirect('/a/lottery/')

        if 'return' in request.POST:
            return redirect('/a/lottery/')

        if 'begin' in request.POST:
            Lottery.objects.filter(id=nid).update(Statue="进行中")
            obj = Lottery.objects.get(id=nid)
            ActivityID = obj.ActivityID
            IDs = obj.IDs
            Name = obj.Name
            Description = obj.Description
            First = obj.First
            Second = obj.Second
            Third = obj.Third
            Special = obj.Special
            Statue = obj.Statue
            return render(request, 'a/Lottery/edit.html',
                          {'ActivityID': ActivityID, 'IDs': IDs, 'Name': Name, 'Description': Description,
                           'First': First, 'Second': Second, 'Third': Third, 'Special': Special, 'Statue': Statue})

        if 'end' in request.POST:
            Lottery.objects.filter(id=nid).update(Statue="结束")
            obj = Lottery.objects.get(id=nid)
            ActivityID = obj.ActivityID
            IDs = obj.IDs
            Name = obj.Name
            Description = obj.Description
            First = obj.First
            Second = obj.Second
            Third = obj.Third
            Special = obj.Special
            Statue = obj.Statue
            return render(request, 'a/Lottery/edit.html',
                          {'ActivityID': ActivityID, 'IDs': IDs, 'Name': Name, 'Description': Description,
                           'First': First, 'Second': Second, 'Third': Third, 'Special': Special, 'Statue': Statue})

        if 'detail' in request.POST:
            Lottery.objects.filter(id=nid).delete()
            return redirect('/a/lottery/')

        return redirect('/a/Lottery/edit/')


def barrage_left(request):
    if request.method == 'GET':
        if not request.user.is_authenticated():
            return redirect('/a/login/')
        else:
            nid = request.GET.get('nid')
            Barrage.objects.filter(id=nid).delete()
            return redirect('/a/barrage/')

    if request.method == 'POST':
        return render(request, 'a/Barrage/left.html')


def barrage_right_detail(request):
    if request.method == 'GET':
        if not request.user.is_authenticated():
            return redirect('/a/login/')
        else:
            nid = request.GET.get('nid')
            Barrage2.objects.filter(id=nid).delete()
            return redirect('/a/barrage/')

    if request.method == 'POST':
        return render(request, 'a/Barrage/right.html')


def barrage_right_create(request):
    if request.method == 'GET':
        if not request.user.is_authenticated():
            return redirect('/a/login/')
        else:
            nid = request.GET.get('nid')
            obj = Barrage2.objects.get(id=nid)
            Barrage.objects.create(Content=obj.Content, Color=obj.Color)
            Barrage2.objects.filter(id=nid).delete()
            return redirect('/a/barrage/')

    if request.method == 'POST':
        return render(request, 'a/Barrage/right.html')