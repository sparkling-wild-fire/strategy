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
from qt_strategy_base.core.common.local_log import local_logger

@singleton
class SchedulerManger:
    def __init__(self):
        self._schedule_thread_event = Event()
        self._global_params = GlobalParams()
        self._callback_message_handler = CallbackMessageHandler()
        self._now_date = datetime.datetime.now().strftime("%Y-%m-%d")
        self._schedule_thread = Thread(target=self.run_job, args=(self._schedule_thread_event,))
        self._job_dict: [str, list] = {}
        self._schedule_thread.start()

    def add_one_schedule(self, target_time: str, function):
        job_id = str(uuid.uuid4())
        if threading.get_ident() == self._callback_message_handler.get_thread_id():
            scheme_id = self._global_params.current_scheme_id
        else:
            scheme_id = 0
        schedule.every().day.at(target_time).do(self.one_task, scheme_id, function).tag(job_id)
        self.add_job_to_dict(job_id=job_id)
        if not self._schedule_thread_event.isSet():
            self._schedule_thread_event.set()
        return job_id

    def add_schedule(self, seconds: int, start_time: str, end_time: str, function):
        error_info = ErrorInfo()
        self._now_date = datetime.datetime.now().strftime("%Y-%m-%d")
        try:          
            start_time = f"{self._now_date } {start_time}"
            job_start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            error_info.set_error_value(error_msg=f"开始时间格式错误:{e}")
            return error_info, None
        try:
            end_time = f"{self._now_date} {end_time}"
            job_end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            error_info.set_error_value(error_msg=f"结束时间格式错误:{e}")
            return error_info, None
        if job_end_time < job_start_time:
            error_info.set_error_value(error_msg="结束时间小于开始时间")
            return error_info, None
        if threading.get_ident() == self._callback_message_handler.get_thread_id():
            scheme_id = self._global_params.current_scheme_id
        else:
            scheme_id = 0
        job_id = str(uuid.uuid4())
        schedule.every(seconds).seconds.do(self.task, scheme_id, job_start_time, job_end_time, function).tag(job_id)
        self.add_job_to_dict(job_id=job_id)
        if not self._schedule_thread_event.isSet():
            self._schedule_thread_event.set()
        return job_id

    def add_job_to_dict(self, job_id: str):
        if threading.get_ident() == self._callback_message_handler.get_thread_id():
            scheme_id = self._global_params.current_scheme_id
        else:
            scheme_id = 0
        job_list: list = self._job_dict.get(scheme_id, None)
        local_logger.info(f"添加定时器{job_id},方案为{scheme_id},获取到的对象为{job_list is None}")
        if job_list is None:
            self._job_dict[scheme_id] = [job_id]
        else:
            job_list.append(job_id)

    def run_job(self, event: Event):
        while True:
            if self._job_dict.values() is None or len(self._job_dict.values()) == 0:
                event.clear()
                event.wait()
            else:
                schedule.run_pending()
                time.sleep(0.1)

    def cancel_schedule(self, scheduler_id: str = None):
        if threading.get_ident() == self._callback_message_handler.get_thread_id():
            scheme_id = self._global_params.current_scheme_id
        else:
            scheme_id = 0
        local_logger.info(f"取消定时器{scheduler_id},方案为{scheme_id}")
        if scheduler_id is not None:
            schedule.clear(scheduler_id)
            job_list: list = self._job_dict.get(scheme_id, None)
            if job_list is not None and scheduler_id in job_list:
                job_list.remove(scheduler_id)
        else:
            self.cancel_scheme_job(scheme_id=scheme_id)

    def cancel_scheme_job(self, scheme_id: int):
        job_list = self._job_dict.get(scheme_id, None)
        if job_list is not None:
            for job_id in job_list:
                schedule.clear(job_id)
            del self._job_dict[scheme_id]

    def _time_covert(self, date: datetime) -> Tuple[int, int, int]:
        hour = date.time().hour
        minute = date.time().minute
        second = date.time().second
        return hour, minute, second

    def one_task(self, scheme_id, job):
        msg_dict = {"function_id": FunctionID.ScheduleCallBack.value, "package_id": 0, "scheme_id": scheme_id,
                    "timestamp": 0, "compression_type": "1", "pack_type": "0",
                    "msg_content": {"schedule_job": job}}
        self._callback_message_handler.add_message(msg_dict)

    def task(self, scheme_id, job_start_time, job_end_time, job):
        now = datetime.datetime.now()
        if job_start_time < now < job_end_time:
            msg_dict = {"function_id": FunctionID.ScheduleCallBack.value, "package_id": 0, "scheme_id": scheme_id,
                        "timestamp": 0, "compression_type": "1", "pack_type": "0",
                        "msg_content": {"schedule_job": job}}
            self._callback_message_handler.add_message(msg_dict)
