# -*- coding: utf-8 -*-

from qt_strategy_base.api.strategy_api import StrategyBase
from qt_strategy_base.core.cache.global_params import GlobalParams
from qt_strategy_base.core.scheme.callback_message_handle import CallbackMessageHandler


class MessageDistribute:
    def __init__(self, message_handler):
        self.message_handler: CallbackMessageHandler = message_handler

    '''
    创建方案消息处理
    '''
    def create_message_handle(self, scheme_id: int, msg_dict: dict):
        from qt_strategy_base.core.scheme.strategy_scheme_impl import ContextImpl
        from qt_strategy_base.core.cache.scheme_manage import SchemeManage
        instance = GlobalParams().strategy
        spi_instance: StrategyBase = instance()
        scheme: ContextImpl = ContextImpl(scheme_id=scheme_id, spi_instance=spi_instance,
                                          message_handler=self.message_handler)
        if scheme:
            SchemeManage().add_scheme(scheme)
            self.message_handler.add_message(msg_dict)

    '''
    停止方案消息处理
    '''
    def stop_message_handle(self, scheme_id: int):
        from qt_strategy_base.core.cache.scheme_manage import SchemeManage
        SchemeManage().remove_scheme(scheme_id)

    '''
    回调消息处理
    '''
    def callback_message_handle(self, msg_dict: dict):
        self.message_handler.add_message(msg_dict)
