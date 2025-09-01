# -- coding: utf-8 --
from qt_strategy_base.core.model.enum import LogSource, EMessageType


class log:
    @staticmethod
    def info(msg):
        from qt_strategy_base.core.common.notice_sever import NoticeServer
        NoticeServer.send_log(message=msg, message_type=EMessageType.INFO.value, log_source=LogSource.CUSTOMER.value)

    @staticmethod
    def debug(msg):
        from qt_strategy_base.core.common.notice_sever import NoticeServer
        NoticeServer.send_log(message=msg, message_type=EMessageType.DEBUG.value, log_source=LogSource.CUSTOMER.value)

    @staticmethod
    def error(msg):
        from qt_strategy_base.core.common.notice_sever import NoticeServer
        NoticeServer.send_log(message=msg, message_type=EMessageType.ERROR.value, log_source=LogSource.CUSTOMER.value)

    @staticmethod
    def warning(msg):
        from qt_strategy_base.core.common.notice_sever import NoticeServer
        NoticeServer.send_log(message=msg, message_type=EMessageType.WARNING.value, log_source=LogSource.CUSTOMER.value)
