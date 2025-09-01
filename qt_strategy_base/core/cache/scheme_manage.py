# -*- coding: utf-8 -*-
from qt_strategy_base.core.common import python_logger
from qt_strategy_base.common.singleton import singleton
from typing import Dict
from qt_strategy_base.core.scheme.strategy_scheme_impl import ContextImpl


@singleton
class SchemeManage:
    def __init__(self):
        self._schemeDict: Dict[int, ContextImpl] = {}

    def add_scheme(self, scheme: ContextImpl):
        self._schemeDict[scheme.scheme_id] = scheme
        scheme.get_async_message_handler().add_scheme(scheme.scheme_id)

    def remove_scheme(self, scheme_id: int):
        scheme: ContextImpl = self._schemeDict.get(scheme_id, None)
        if scheme:
            scheme.get_async_message_handler().remove_scheme(scheme_id)
            del self._schemeDict[scheme_id]

    def get_scheme(self, scheme_id: int) -> ContextImpl:
        scheme = self._schemeDict.get(scheme_id, None)
        if not scheme:
            python_logger.warning(f"找不到方案：{scheme}")
        return scheme

    def get_first_scheme(self):
        scheme_list = self._schemeDict.values()
        if len(scheme_list) > 0:
            return next(iter(scheme_list))
        else:
            return None

    def get_scheme_num(self) -> int:
        return len(self._schemeDict)
