"""Administrator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from Administrator_ import views
from django.conf.urls import url

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^a/login/', views.llogin),
    url(r'^a/logout/', views.Logout),
    url(r'^a/register/', views.register),
    url(r'^a/activity/', views.activity),
    url(r'^a/lottery/', views.lottery),
    url(r'^a/barrage/', views.barrage),
    url(r'^a/Lottery/create/', views.lottery_create),
    url(r'^a/Lottery/edit/', views.lottery_edit),
    url(r'^a/Activity/create/', views.activity_create),
    url(r'^a/Activity/down/', views.activity_down),
    url(r'^a/Activity/edit/', views.activity_edit),
    url(r'^a/Activity/up/', views.activity_up),
    url(r'^a/Barrage/left/', views.barrage_left),
    url(r'^a/Barrage/right_detail/', views.barrage_right_detail),
    url(r'^a/Barrage/right_create/', views.barrage_right_create),
]
