# -- coding: utf-8 --
from qt_strategy_base.core.model.enum import EMessageType


def error(msg):
    from qt_strategy_base.core.common.notice_sever import NoticeServer
    NoticeServer.send_log(message=str(msg), message_type=EMessageType.ERROR.value)


def warning(msg):
    from qt_strategy_base.core.common.notice_sever import NoticeServer
    NoticeServer.send_log(message=str(msg), message_type=EMessageType.WARNING.value)


def info(msg):
    from qt_strategy_base.core.common.notice_sever import NoticeServer
    NoticeServer.send_log(message=str(msg), message_type=EMessageType.INFO.value)


def debug(msg):
    from qt_strategy_base.core.common.notice_sever import NoticeServer
    NoticeServer.send_log(message=str(msg), message_type=EMessageType.DEBUG.value)
