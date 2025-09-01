# -*- coding: UTF-8 -*
from pandas import DataFrame

from qt_strategy_base.core.scheme.strategy_scheme_stock_impl import SecurityDetail
from qt_strategy_base.model.enum import SchemeType


class SchemeInfo:
    def get_scheme_id(self) -> int:
        """
        获取方案号
        @return: 方案号
        """

    def get_internal_orders(self, internal_ids: list[str] = None) -> DataFrame:
        """
        获取当前内部委托
        @param internal_ids: 内部委托号
        @return:委托数据DataFrame
        """
        pass

    def get_parameters(self) -> dict:
        """
        获取方案参数
        @return:方案参数
        """
        pass

    def get_security_list(self) -> list[str]:
        """
        获取方案券池
        @return: 方案券池
        """
        pass

    def get_status(self) -> SchemeType:
        """
        获取方案状态
        @return: 方案状态
        """
        pass

    def get_security_details(self) -> list[SecurityDetail]:
        """
        获取方案明细列表
        @return: 方案明细列表
        """
        pass

    def get_security_detail_by_id(self, id) -> SecurityDetail:
        """
        通过明细号获取方案明细
        @param id: 明细号
        @return: 方案明细
        """
        pass

    def get_security_details_by_security(self, security) -> list[SecurityDetail]:
        """
        通过证券代码获取方案明细
        @param security: 证券代码
        @return: 方案明细列表
        """
        pass


class Indicator:

    def add(self, key: str, value: [str, float, int, bool], unit: str = "", order: int = 0):
        """
        添加或者更新指标
        @param key: 指标主键
        @param value: 指标值
        @param unit: 单位
        @param order: 顺序
        @return:
        """
        pass

    def push(self):
        """
        推送指标
        @return:
        """
        pass


class ContextInfo:
    @property
    def scheme(self) -> SchemeInfo:
        """
        方案
        @return:
        """
        pass

    def indicator(self) -> Indicator:
        """
        指标
        @return:
        """
        pass
