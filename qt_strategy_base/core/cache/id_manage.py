# -*- coding: utf-8 -*-
from threading import Lock
from qt_strategy_base.core.cache.global_params import GlobalParams
from qt_strategy_base.common.singleton import singleton


@singleton
class PackageIdManager:
    def __init__(self):
        self._package_id = 0

    def get_package_id(self) -> int:
        self._package_id = self._package_id + 1
        return self._package_id


@singleton
class OrderIdManager:
    def __init__(self):
        self._status = True
        self._order_id_start = ""
        self._order_id_end = 0
        self._lock = Lock()

    @property
    def order_id_start(self) -> str:
        return self._order_id_start

    @order_id_start.setter
    def order_id_start(self, value):
        self._order_id_start: str = value

    def update_order_id_start(self, new_order_id_start) -> str:
        self._order_id_start = new_order_id_start
        self._status = True
        return GlobalParams().strategy_id + "#" + self._order_id_start + "_" + str(self._order_id_end).zfill(5)

    def get_order_id(self) -> (bool, str):
        self._lock.acquire()
        try:
            if self._order_id_end <= 9999 and self._order_id_end != 0:
                self._order_id_end = self._order_id_end + 1
                order_id = GlobalParams().strategy_id + "#" + self._order_id_start + "_" + str(
                    self._order_id_end).zfill(5)
                return self._status, order_id
            else:
                self._status = False
                self._order_id_end = 1
                return self._status, ""
        finally:
            self._lock.release()
