from django.db import models


class Lottery(models.Model):
    ActivityID = models.IntegerField(default=0)
    IDs = models.IntegerField(default=0)
    Name = models.CharField(max_length=30)
    Description = models.CharField(max_length=100)
    First = models.IntegerField(default=0)
    Second = models.IntegerField(default=0)
    Third = models.IntegerField(default=0)
    Special = models.IntegerField(default=0)
    Statue = models.CharField(max_length=20)


class Barrage(models.Model):
    Content = models.CharField(max_length=100)
    Color = models.CharField(max_length=100)


class Barrage2(models.Model):
    Content = models.CharField(max_length=100)
    Color = models.CharField(max_length=100)


class Activity(models.Model):
    ActivityID = models.IntegerField(default=0)
    Name = models.CharField(max_length=30)
    Organnizer = models.CharField(max_length=30)
    Description = models.CharField(max_length=100)
    PirUrl = models.ImageField()
    StartTime = models.TimeField()
    EndTime = models.TimeField()
    BgPicUrl = models.ImageField()
    Statue = models.CharField(max_length=20)
