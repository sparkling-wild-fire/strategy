# -- coding: utf-8 --
from qt_strategy_base.api.strategy_api_context import Indicator
from qt_strategy_base.core.common.notice_sever import NoticeServer


class Indicator(Indicator):
    def __init__(self, scheme):
        self._scheme = scheme
        self._key_value_dict = {}

    def add(self, key: str, value: [str, float, int, bool], unit: str = "", order: int = 0):
        scheme_ins_code: str = ""
        index = f"{self._scheme.scheme_id}-{scheme_ins_code}-{key}"
        self._key_value_dict[index] = (key, str(value), unit, order, str(scheme_ins_code))

    def push(self):
        push_info = []
        for k, v in self._key_value_dict.items():
            push_info.append([v[0], v[1], v[2], v[3], v[4]])
        NoticeServer.push_key_value_count(scheme_id=self._scheme.get_scheme_id(), key_value_info=push_info)
        self._key_value_dict.clear()

