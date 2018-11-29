# -*- coding: utf-8 -*-
#
from wechat.wrapper import WeChatHandler
from wechat.models import *
from django.utils import timezone
__author__ = "Epsirom"


class ErrorHandler(WeChatHandler):

    def check(self):
        return True

    def handle(self):
        return self.reply_text('对不起，服务器现在有点忙，暂时不能给您答复 T T')


class DefaultHandler(WeChatHandler):

    def check(self):
        return True

    def handle(self):
        return self.reply_text('对不起，没有找到您需要的信息:(')


class HelpOrSubscribeHandler(WeChatHandler):

    def check(self):
        return self.is_text('帮助', 'help') or self.is_event('scan', 'subscribe') or \
               self.is_event_click(self.view.event_keys['help'])

    def handle(self):
        return self.reply_single_news({
            'Title': self.get_message('help_title'),
            'Description': self.get_message('help_description'),
            'Url': self.url_help(),
        })


class UnbindOrUnsubscribeHandler(WeChatHandler):

    def check(self):
        return self.is_text('解绑') or self.is_event('unsubscribe')

    def handle(self):
        self.user.student_id = ''
        self.user.save()
        return self.reply_text(self.get_message('unbind_account'))


class BindAccountHandler(WeChatHandler):

    def check(self):
        return self.is_text('绑定') or self.is_event_click(self.view.event_keys['account_bind'])

    def handle(self):
        return self.reply_text(self.get_message('bind_account'))


class BookEmptyHandler(WeChatHandler):

    def check(self):
        return self.is_event_click(self.view.event_keys['book_empty'])

    def handle(self):
        return self.reply_text(self.get_message('book_empty'))

class GetTicketHandler(WeChatHandler):

    def check(self):
        return self.is_text('查票') or self.is_event_click(self.view.event_keys['get_ticket'])

    def handle(self):

        if not self.user.student_id:
            return self.reply_text(self.get_message('bind_account'))
        tickets = Ticket.objects.filter(student_id=self.user.student_id)
        if not len(tickets):
            return self.reply_text("No tickets")
        return self.reply_news([{ 'Title':ticket.activity.name,
                                    'Description':ticket.activity.description,
                                  'PicUrl':ticket.activity.pic_url,
                                  'Url':self.url_ticket(ticket.unique_id)
                                  }for ticket in tickets])

class BookTicketHandle(WeChatHandler):
    def check(self):
        return self.is_in_text('抢票')

    def handle(self):
        if not self.user.student_id:
            return self.reply_text(self.get_message('bind_account'))
        ids = self.input['Content'].split(' ')
        if len(ids) == 1:
            return self.reply_text('Please input Activity ID')
        id = ids[1]
        activity = Activity.objects.filter(key=id)
        if (len(activity)):
            activity = activity[0]
            if len(Ticket.objects.filter(student_id=self.user.student_id, activity=activity)):
                return self.reply_text("You Already Have One")
            if activity.book_start >= timezone.now():
                return self.reply_text("Book Has Not Start Yet")
            if activity.book_end <= timezone.now():
                return  self.reply_text("Book Has Ended")
            if activity.remain_tickets <= 0:
                return self.reply_text("No Tickets left")
            activity.remain_tickets -= 1
            activity.save()

            ticket = Ticket.objects.create(student_id=self.user.student_id,activity=activity,status=Ticket.STATUS_VALID,unique_id=Ticket.generate_unique_id())
            ticket.save()
            return self.reply_text('抢票成功')
        else:
            return self.reply_text('No Such Activity ID')

class BookWhatHandler(WeChatHandler):
    def check(self):
        return self.is_text("抢啥") or self.is_event_click(self.view.event_keys['book_what'])
    def handle(self):
        print("book what")
        if not self.user.student_id:
            return self.reply_text(self.get_message('bind_account'))
        activities = Activity.objects.filter(status = Activity.STATUS_PUBLISHED,book_end__gt=timezone.now()).order_by('-book_end')

        if len(activities):
            output = []
            for activity in activities:
                output.append({
                    'Title':activity.name,
                    'Description':activity.description,
                    'PicUrl':activity.pic_url,
                    'Url':self.url_activity(activity.id)
                })
                return self.reply_news(output)
        else:
            return self.reply_text(self.get_message('book_empty'))

class CancelTicketHandler(WeChatHandler):
    def check(self):
        return self.is_in_text('退票')
    def handle(self):
        if not self.user.student_id:
            return self.reply_text(self.get_message('bind_account'))
        ids = self.input['Content'].split(' ')
        if len(ids) == 1:
            return self.reply_text('Please input Activity ID')
        id = ids[1]


        activity = Activity.objects.filter(key=id)
        if not len(activity):
            return self.reply_text('No Such Activity')
        activity = activity[0]
        ticket = Ticket.objects.filter(student_id=self.user.student_id,activity= activity)
        if not len(ticket):
            return self.reply_text("Not Valid Ticket ID")
        ticket = ticket[0]
        if ticket.status != Ticket.STATUS_VALID:
            return  self.reply_text("Invalid Ticket")
        ticket.status = Ticket.STATUS_CANCELLED
        ticket.activity.remain_tickets += 1
        return self.reply_text('Succeed in refund')


#需要一个输入参数，可以是unique_id也可以是key
class CheckTicketHandler(WeChatHandler):
    def check(self):
        return self.is_in_text('检票')
    def handle(self):
        ids = self.input['Content'].split(' ')
        if len(ids) == 1:
            return self.reply_text('Please Input Unique ID')
        id = ids[1]
        print(id)
        activity = Activity.objects.filter(key=id)
        if not(len(activity)):

            ticket = Ticket.objects.filter(unique_id=id)
        else:
            activity = activity[0]
            ticket = Ticket.objects.get(activity=activity)
        if ticket.student_id != self.user.student_id:
            return self.reply_text("It Is Not Your Ticket")
        if ticket.status != Ticket.STATUS_VALID:
            return self.reply_text("Invalid Ticket")
        if ticket.activity.status != Activity.STATUS_PUBLISHED:
            return self.reply_text("No Such Activity")
        ticket.status = Ticket.STATUS_USED
        return self.reply_text("Check Success")



