from django.db import models
import random,string
from codex.baseerror import LogicError


class User(models.Model):
    open_id = models.CharField(max_length=64, unique=True, db_index=True)
    student_id = models.CharField(max_length=32, unique=True, db_index=True)

    @classmethod
    def get_by_openid(cls, openid):
        try:
            return cls.objects.get(open_id=openid)
        except cls.DoesNotExist:
            raise LogicError('User not found')


class Activity(models.Model):
    name = models.CharField(max_length=128)
    key = models.CharField(max_length=64, db_index=True)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    place = models.CharField(max_length=256)
    book_start = models.DateTimeField(db_index=True)
    book_end = models.DateTimeField(db_index=True)
    total_tickets = models.IntegerField()
    status = models.IntegerField()
    pic_url = models.CharField(max_length=256)
    remain_tickets = models.IntegerField()

    STATUS_DELETED = -1
    STATUS_SAVED = 0
    STATUS_PUBLISHED = 1

    @classmethod
    def get_by_id(cls,id):
        try:
            return cls.objects.get(id=id)
        except cls.DoesNotExist:
            raise LogicError("Activity not found")

    @classmethod
    def get_status_ge_0(cls):
        try:
            return cls.objects.filter(status__gte = 0)
        except cls.DoesNotExist:
            raise LogicError('Activity Not Found')

class Ticket(models.Model):
    student_id = models.CharField(max_length=32, db_index=True)
    unique_id = models.CharField(max_length=64, db_index=True, unique=True)
    activity = models.ForeignKey(Activity)
    status = models.IntegerField()

    @classmethod
    def generate_unique_id(cls):
        temp = ''.join(random.sample(string.ascii_letters + string.digits,32))

        while 1:
            print('loop')
            temp = ''.join(random.sample(string.ascii_letters + string.digits, 32))
            t = cls.objects.filter(unique_id=temp)
            if(not len(t)):
                return temp


    STATUS_CANCELLED = 0
    STATUS_VALID = 1
    STATUS_USED = 2
