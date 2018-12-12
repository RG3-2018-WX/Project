"""DjangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from adminpage import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^a/login/', views.login),
    url(r'^a/logout/', views.Logout),
    url(r'^a/register/', views.Register),
    url(r'^a/activity/', views.ActivityList),
    url(r'^a/lottery/', views.LotteryList),
    url(r'^a/barrage/', views.SetComment),
    url(r'^a/Lottery/create/', views.LotteryCreate),
    url(r'^a/Lottery/edit/', views.LotteryDetail),
    url(r'^a/Activity/create/', views.ActivityCreate),
    url(r'^a/Activity/edit/', views.ActivityDetail),
    url(r'^a/Activity/delete/', views.ActivityDelete),
    url(r'^a/Barrage/left/', views.barrage_left_detele),
    url(r'^a/Barrage/left_create/', views.barrage_left_create),
    url(r'^a/Barrage/right_detail/', views.barrage_right_detele,
    url(r'^a/Barrage/right_create/', views.barrage_right_create,
    url(r'^a/Programe/delete/', views.ProgrameDelete),
    url(r'^a/Programe/up/', views.ProgrameUp),
    url(r'^a/Programe/down/', views.ProgrameDown),
    url(r'^a/Programe/create/', views.ProgrameCreate),
    url(r'^a/Programe/edit/', views.ProgrameDetail),
]
