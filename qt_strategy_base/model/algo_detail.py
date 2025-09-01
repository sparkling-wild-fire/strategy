# -- coding: utf-8 --
from abc import ABC
from typing import Tuple

from pandas import DataFrame

from qt_strategy_base.model.error_info import ErrorInfo
from qt_strategy_base.core.scheme.strategy_order_impl import OrderData
from qt_strategy_base.model.enum import Side, CloseType, Direction, ControlType, SecurityDetailStatus
from qt_strategy_base.model.strategy_api_data import AccountInfo
from qt_strategy_base.core.model.base import BaseObject


class AlgoDetail(BaseObject, ABC):

    @property
    def id(self) -> str:
        """
        证券明细号
        """
        pass

    @property
    def security(self) -> str:
        """
        证券明细代码
        """
        pass

    @property
    def side(self) -> Side:
        """
        委托方向
        """
        pass

    @property
    def direction(self) -> Direction:
        """
        开平方向
        """
        pass

    @property
    def target_quantity(self) -> float:
        """
        目标数量
        """
        pass

    @property
    def control_type(self) -> ControlType:
        """
        控制类型
        """
        pass

    @property
    def total_volume(self) -> float:
        """
        累计成交数量
        """
        pass

    @property
    def total_value(self) -> float:
        """
        累计成交金额
        """
        pass

    @property
    def status(self) -> SecurityDetailStatus:
        """
        明细状态
        """
        pass

    @property
    def order_quantity(self) -> float:
        """
        累计委托数量
        """
        pass

    @property
    def order_value(self) -> float:
        """
        累计委托金额
        """
        pass

    def get_account(self) -> AccountInfo:
        """
        获取当前明细的账户
        @return:AccountInfo
        """
        pass

