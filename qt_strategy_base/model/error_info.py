# -*- coding: utf-8 -*-
from qt_strategy_base.core.common.constant import ApiRetType


class ErrorInfo:
    def __init__(self, error_no=ApiRetType.APIRETOK.value, error_msg=""):
        self._error_no: int = error_no
        self._error_msg: str = error_msg

    @property
    def error_no(self) -> int:
        return self._error_no

    @error_no.setter
    def error_no(self, value):
        self._error_no = value

    @property
    def error_msg(self) -> str:
        return self._error_msg

    @error_msg.setter
    def error_msg(self, value):
        self._error_msg = value

    def set_value(self, error_no, error_msg):
        self._error_no = error_no
        self._error_msg = error_msg

    def set_error_value(self, error_msg, error_no=ApiRetType.APIRETERR.value):
        self._error_no = error_no
        self._error_msg = error_msg

    def has_error(self):
        if self._error_no != ApiRetType.APIRETOK.value:
            return True
        else:
            return False

    @staticmethod
    def bad(error_msg):
        error_info = ErrorInfo()
        error_info._error_no = ApiRetType.APIRETERR.value
        error_info.error_msg = error_msg
        return error_info

    @staticmethod
    def ok():
        error_info = ErrorInfo()
        error_info._error_no = ApiRetType.APIRETOK.value
        return error_info

