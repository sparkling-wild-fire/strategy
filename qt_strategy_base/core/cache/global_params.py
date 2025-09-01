# -*- coding: utf-8 -*-
from qt_strategy_base.model.enum import ExecuteMode
from qt_strategy_base.common.singleton import singleton


@singleton
class GlobalParams:
    def __init__(self):
        self._execute_mode = ExecuteMode.Run
        self._strategy_id = ""
        self._strategy_name = ""
        self._strategy = ""
        self._process_uuid = ""
        self._ip_address = ""
        self._port = 0
        self._log_level = "1"
        self._current_scheme_id = 0

    @property
    def strategy_id(self) -> str:
        return self._strategy_id

    @strategy_id.setter
    def strategy_id(self, value):
        self._strategy_id = value

    @property
    def current_scheme_id(self) -> int:
        return self._current_scheme_id

    @current_scheme_id.setter
    def current_scheme_id(self, value):
        self._current_scheme_id = value

    @property
    def strategy_name(self) -> str:
        return self._strategy_name

    @strategy_name.setter
    def strategy_name(self, value):
        self._strategy_name = value

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, value):
        self._strategy = value

    @property
    def process_uuid(self) -> str:
        return self._process_uuid

    @process_uuid.setter
    def process_uuid(self, value):
        self._process_uuid = value

    @property
    def ip_address(self) -> str:
        return self._ip_address

    @ip_address.setter
    def ip_address(self, value):
        self._ip_address = value

    @property
    def port(self) -> int:
        return self._port

    @port.setter
    def port(self, value):
        self._port = value

    @property
    def log_level(self) -> str:
        return self._log_level

    @log_level.setter
    def log_level(self, value):
        self._log_level = value

    @property
    def execute_mode(self) -> ExecuteMode:
        return self._execute_mode

    @execute_mode.setter
    def execute_mode(self, value):
        self._execute_mode = value
