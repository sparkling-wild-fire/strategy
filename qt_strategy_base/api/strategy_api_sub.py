# -- coding: utf-8 --
from typing import Tuple, List

from qt_strategy_base import ClearSpeed
from qt_strategy_base.core.common.aglo_function_impl import FunctionImpl
from qt_strategy_base.model.error_info import ErrorInfo


def sub_snapshot(security_list: list[str]) -> ErrorInfo:
    """
    订阅行情
    @param security_list: 券的列表，如["600570.XSHG","600000.XSHG"]
    @return: 错误信息
    对应回调函数on_snapshot(self, context: ContextInfo, snapshot_data:SnapshotData)
    """
    return FunctionImpl.sub_snapshot(security_list=security_list)


def sub_position(security_accountInfo_list: List[Tuple]) -> ErrorInfo:
    """
    根据券和账户订阅持仓
    @param security_accountInfo_list: 券和账户的元组构成的列表，如[("600570.XSHG",account_info)]
    @return:错误信息
    对应回调函数on_position(self, context: ContextInfo, position_data: PositionData)
    """
    return FunctionImpl.sub_position(security_account_list=security_accountInfo_list)


def sub_order(security_accountInfo_list: List[Tuple]) -> ErrorInfo:
    """
    订阅外部委托信息
    @param security_accountInfo_list:券和账户的元组构成的列表，如[("600570.XSHG",account_info)]
    @return:错误信息
    对应回调函数on_order(self, context: ContextInfo, order_data: OrderData, push_type: PushType)
    """

    return FunctionImpl.sub_order(security_account_list=security_accountInfo_list)


def sub_trade(security_accountInfo_list: List[Tuple]) -> ErrorInfo:
    """
    订阅外部成交信息
    @param security_accountInfo_list:券和账户的元组构成的列表，如[("600570.XSHG",account_info)]
    @return:错误信息
    对应回调函数(self, context: ContextInfo, trade: TradeData)
    """
    return FunctionImpl.sub_trade(security_account_list=security_accountInfo_list)


def sub_comb_order(security_accountInfo_list: List[Tuple]) -> ErrorInfo:
    """
    订阅合笔委托
    @param security_accountInfo_list:券和账户的元组构成的列表，如[("600570.XSHG",account_info)]
    @return: 错误信息
    对应回调函数on_comb_order(self, context: ContextInfo, comb_order_data:CombOrderData, push_type:PushType)
    """
    return FunctionImpl.sub_comb_order(security_account_list=security_accountInfo_list)


def sub_market_duty(security_list: list[str]) -> ErrorInfo:
    """
    订阅做市义务
    @param security_list:证券列表
    @return:错误信息
    对应回调函数on_market_duty(self, context: ContextInfo, market_duty_info: MarketDutyData)
    """
    return FunctionImpl.sub_market_duty(security_list=security_list)


def sub_factor(security_list: list[str], factor_name: str) -> ErrorInfo:
    """
    订阅做市义务
    @param security_list:证券列表
    @param factor_name:因子名称
    @return:错误信息
    对应回调函数on_factor(self, context: ContextInfo, factor_info: Factor)
    """
    return FunctionImpl.sub_factor(security_list=security_list, factor=factor_name)


def sub_bond_click_hq(security_list: list[str], clear_speed=None) -> ErrorInfo:
    """
    订阅债券点击行情
    @param security_list:证券列表
    @param clear_speed:清算速度，上交所只能是T1，深交所可以是T1或T0
    @return:错误信息
    对应回调函数on_bond_click_hq(self, context: ContextInfo,bond_click_hq:BondClickHq)
    """
    return FunctionImpl.bond_click_hq(security_list=security_list, clear_speed=clear_speed)


def sub_xbond(security_list: list[str], clear_speed: ClearSpeed = None) -> ErrorInfo:
    """
    订阅Xbond行情
    @param security_list:证券列表
    @param clear_speed: 清算速度
    @return:错误信息
    对应回调函数on_xbond(self, context: ContextInfo, xbond_hq:XBondInfo)
    """
    return FunctionImpl.sub_xbond(security_list=security_list, clear_speed=clear_speed)


def sub_intrabak_bond_mm(security_list: list[str], clear_speed: ClearSpeed = None) -> ErrorInfo:
    """
    订阅银行间做市行情
    @param security_list:证券列表
    @param clear_speed: 清算速度
    @return:错误信息,
    对应回调函数on_intrabak_bond_mm(self, context: ContextInfo, yhj_hq:YHJBondMMInfo)
    """
    return FunctionImpl.sub_intrabak_bond_mm(security_list=security_list, clear_speed=clear_speed)


def unsub_snapshot() -> ErrorInfo:
    """
    取消行情订阅
    @return: 错误信息
    """
    return FunctionImpl.unsub_snapshot()


def unsub_position() -> ErrorInfo:
    """
    取消持仓订阅
    @return:错误信息
    """
    return FunctionImpl.unsub_position()


def unsub_order() -> ErrorInfo:
    """
    取消委托订阅
    @return:错误信息
    """

    return FunctionImpl.unsub_order()


def unsub_trade() -> ErrorInfo:
    """
    取消成交订阅
    @return:错误信息
    """
    return FunctionImpl.unsub_trade()


def unsub_market_duty() -> ErrorInfo:
    """
    取消做市义务订阅
    @return:错误信息
    """
    return FunctionImpl.unsub_market_duty()


def unsub_factor() -> ErrorInfo:
    """
    取消因子订阅
    @return:错误信息
    """
    return FunctionImpl.unsub_factor()


def unsub_bond_click_hq() -> ErrorInfo:
    """
    取消债券点击行情订阅
    @return: 错误信息
    """
    return FunctionImpl.unsub_bond_click_hq()


def unsub_comb_order() -> ErrorInfo:
    """
    取消合笔委托订阅
    @return: 错误信息
    """
    return FunctionImpl.unsub_comb_order()


def unsub_xbond() -> ErrorInfo:
    """
    取消xbond行情订阅
    @return: 错误信息
    """
    return FunctionImpl.unsub_xbond()


def unsub_intrabank_bond_mm() -> ErrorInfo:
    """
    取消银行间做市行情订阅
    @return: 错误信息
    """
    return FunctionImpl.unsub_intrabank_bond_mm()
