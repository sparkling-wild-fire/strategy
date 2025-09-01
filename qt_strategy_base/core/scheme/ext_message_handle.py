# -*- coding: utf-8 -*-
import threading
import time
import uuid
import datetime
from threading import Thread, Event
from typing import Any, Tuple
import schedule

from qt_strategy_base.model import ErrorInfo
from qt_strategy_base.core.cache.global_params import GlobalParams

from qt_strategy_base.core.common.constant import FunctionID
from qt_strategy_base.common.singleton import singleton
from qt_strategy_base.core.scheme.callback_message_handle import CallbackMessageHandler


@singleton
class ExtMessageManager:
    def __init__(self):
        self._global_params = GlobalParams()
        self._callback_message_handler = CallbackMessageHandler()

    def message_push(self, data):
        if threading.get_ident() == self._callback_message_handler.get_thread_id():
            scheme_id = self._global_params.current_scheme_id
            msg_dict = {"function_id": FunctionID.ExtMessageCallBack.value, "package_id": 0, "scheme_id": scheme_id,
                        "timestamp": 0, "compression_type": "1", "pack_type": "0",
                        "msg_content": {"ext_data": data}}
            self._callback_message_handler.add_message(msg_dict)
