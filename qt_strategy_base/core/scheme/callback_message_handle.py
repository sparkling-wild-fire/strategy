# -*- coding: utf-8 -*-
import queue
import threading
import time
import traceback
from threading import Thread, Event
from typing import List

from qt_strategy_base.core.cache.global_params import GlobalParams
from qt_strategy_base.core.common import python_logger
from qt_strategy_base.core.common.local_log import local_logger
from qt_strategy_base.common.singleton import singleton
from qt_strategy_base.core.common.notice_sever import NoticeServer
from qt_strategy_base.core.common.public_func import msg_package_covert


@singleton
class CallbackMessageHandler:
    def __init__(self):
        self._handle_scheme_list: List[int] = []  # 需要处理的方案id
        self._message_queues = queue.Queue()
        self._message_handle_thread_event = Event()
        self._message_handle_thread = Thread(target=self.callback_message_handle)
        self._message_handle_thread.start()
        self._global_param = GlobalParams()
        self._exception_num = 0

    # 获取线程id
    def get_thread_id(self) -> int:
        return self._message_handle_thread.ident

    # 当前线程正在处理的消息所属的方案的方案id
    def set_current_scheme_id(self, scheme_id):
        self._global_param.current_scheme_id = scheme_id

    # 获取线程状态
    def get_handle_thread_status(self):
        return self._message_handle_thread.is_alive()

    # 检查线程状态，如果线程状态异常重新创建一个
    def check_thread_status(self):
        if not self._message_handle_thread.is_alive():
            self._message_handle_thread = Thread(target=self.callback_message_handle)
            self._message_handle_thread.start()

    # 线程等待，time_out，单位秒
    def thread_wait(self, time_out: int):
        self._message_handle_thread_event.clear()
        self._message_handle_thread_event.wait(time_out)

    # 线程恢复运行
    def thread_resume(self):
        self._message_handle_thread_event.set()

    # 添加一个需要进行消息处理的方案
    def add_scheme(self, scheme_id: int):
        self._handle_scheme_list.append(scheme_id)

    # 删除一个需要进行消息处理的方案
    def remove_scheme(self, scheme_id: int):
        self._handle_scheme_list.remove(scheme_id)

    # 需要进行消息处理的方案个数
    def get_scheme_list_length(self) -> int:
        return len(self._handle_scheme_list)

    # 添加一个待处理的消息到队列中
    def add_message(self, msg_dict: dict):
        self._message_queues.put(msg_dict)

    # 获取队列中的消息个数
    def get_message_num(self) -> int:
        return self._message_queues.qsize()

    # 监控消息队列
    def callback_message_handle(self):
        while True:
            if not self._message_queues.empty():
                msg_dict: dict = self._message_queues.get()
                python_logger.debug("callback_message_handle函数调用")
                python_logger.debug(msg_dict)
                function_id: int = msg_dict.get("function_id", 0)
                scheme_id: int = msg_dict.get("scheme_id", 0)
                package_id: str = msg_dict.get("package_id", 0)
                pack_type: int = msg_dict.get("pack_type", 0)
                body: str = msg_dict.get("msg_content", None)
                if body is None:
                    continue
                msg_package_covert(msg_dict)
                self.set_current_scheme_id(scheme_id)
                try:
                    if scheme_id == 0:
                        from qt_strategy_base.core.scheme.fuction_collection import FunctionInfo, FUNCTION_INFO_DICT
                        function_info: FunctionInfo = FUNCTION_INFO_DICT.get(function_id, None)
                        function_info.function(None, msg_dict)
                    else:
                        from qt_strategy_base.core.cache.scheme_manage import SchemeManage
                        from qt_strategy_base.core.scheme.strategy_scheme_impl import ContextImpl
                        scheme: ContextImpl = SchemeManage().get_scheme(scheme_id)
                        if scheme is not None:
                            from qt_strategy_base.core.scheme.fuction_collection import FunctionInfo, \
                                FUNCTION_INFO_DICT
                            function_info: FunctionInfo = FUNCTION_INFO_DICT.get(function_id, None)
                            function_info.function(scheme, msg_dict)
                except Exception as e:
                    local_logger.error(
                        f"消息处理线程异常!线程id：{threading.currentThread().ident}，消息内容：{msg_dict},错误原因:{str(e)}")
                    ("消息处理线程异常!" + str(e))
                    local_logger.error(traceback.format_exc())
                    print(traceback.format_exc())
                    NoticeServer.thread_exception_handle(scheme_id=scheme_id, package_id=package_id,
                                                         exception_cause=str(e),
                                                         thread_id=threading.currentThread().ident)

            else:
                time.sleep(0)
