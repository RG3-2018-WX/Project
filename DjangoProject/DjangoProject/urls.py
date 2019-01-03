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
from django.conf.urls import url,include
from django.contrib import admin
from adminpage import views
from barragepage import views as views2
from userpage import views as u_view
from django.views.static import serve
from userpage import views as u_view
from django.conf.urls.static import static
from DjangoProject import settings

urlpatterns = [
	url(r'^a/',include('adminpage.urls') ),
	url(r'^b/',include('adminpage.urls') ),
    url(r'^$', views.Login.as_view()),
    url(r'^BarrierWall/', views2.BarrierWall.as_view()),
    url(r'^m/(?P<path>.*)$', serve, {'document_root': 'static/'}),
	url(r'^api/u/',include('userpage.urls') ),
   
]
