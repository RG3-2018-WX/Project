from django.utils import timezone

from wechat.wrapper import WeChatView, WeChatLib
from wechat.handlers import *
from wechat.models import Activity
from DjangoProject.settings import WECHAT_TOKEN, WECHAT_APPID, WECHAT_SECRET


class CustomWeChatView(WeChatView):

    lib = WeChatLib(WECHAT_TOKEN, WECHAT_APPID, WECHAT_SECRET)

    handlers = [
        HelpOrSubscribeHandler, UnbindOrUnsubscribeHandler, BindAccountHandler, BookEmptyHandler, GetTicketHandler,
        BookTicketHandle,BookWhatHandler,CancelTicketHandler,CheckTicketHandler
    ]
    error_message_handler = ErrorHandler
    default_handler = DefaultHandler

    event_keys = {
        'book_what': 'SERVICE_BOOK_WHAT',
        'get_ticket': 'SERVICE_GET_TICKET',
        'account_bind': 'SERVICE_BIND',
        'help': 'SERVICE_HELP',
        'book_empty': 'BOOKING_EMPTY',
        'book_header': 'BOOKING_ACTIVITY_',
    }

    menu = {
        'button': [
            {
                "name": "服务",
                "sub_button": [
                    {
                        "type": "click",
                        "name": "抢啥",
                        "key": event_keys['book_what'],
                    },
                    {
                        "type": "click",
                        "name": "查票",
                        "key": event_keys['get_ticket'],
                    },
                    {
                        "type": "click",
                        "name": "绑定",
                        "key": event_keys['account_bind'],
                    },
                    {
                        "type": "click",
                        "name": "帮助",
                        "key": event_keys['help'],
                    }
                ]
            },
            {
                "name": "抢票",
                "sub_button": []
            }
        ]
    }
