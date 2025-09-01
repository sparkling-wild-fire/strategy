# -- coding: utf-8 --
from abc import ABC
from qt_strategy_base.model.error_info import ErrorInfo
from qt_strategy_base.model.strategy_api_data import AccountInfo
from qt_strategy_base.model.enum import Direction, Side, SchemeType
from qt_strategy_base.core.model.base import BaseObject


class AlgoScheme(BaseObject, ABC):
    def get_status(self) -> SchemeType:
        """
        获取方案状态
        @return:
        """
        pass

    def get_param_info(self) -> dict:
        """
        获取方案参数信息key为参数名称，value为参数类型I代表int，C代表char，S代表string，D代表float
        @return:
        """
        pass

    def set_param(self, param_name, value):
        """
        设置参数
        @param param_name: 参数名称
        @param value: 参数值
        @return:
        """
        pass

    def add_security_detail(self, security: str, account_info: AccountInfo, side: Side = None,
                            direction: Direction = None,
                            target_quantity: float = None,
                            target_value: float = None):
        """
        添加明细
        @param security:证券名称
        @param account_info:账户信息
        @param side:委托方向
        @param direction:开平仓方向
        @param target_quantity:目标数量
        @param target_value:目标金额
        @return:
        """
        pass

    def run(self) -> ErrorInfo:
        """
        algo方案运行
        @return:错误信息
        """
        pass

    def cancel(self) -> ErrorInfo:
        """
        algo方案撤销
        @return:错误信息
        """
        pass
