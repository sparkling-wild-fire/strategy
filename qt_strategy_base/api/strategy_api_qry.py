# -*- coding: utf-8 -*-
from typing import List, Tuple, Dict
from pandas import DataFrame

from qt_strategy_base.model.enum import AccountType
from qt_strategy_base.core.common.aglo_function_impl import FunctionImpl
from qt_strategy_base.model.error_info import ErrorInfo
from qt_strategy_base.model.strategy_api_data import SecurityBaseInfo, StockBaseInfo, BondBaseInfo, FuturesBaseInfo, \
    OptionBaseInfo, ETFInfo, AccountInfo, AccountFund, Factor, BondCalcData


def get_position(security_account_list: List[Tuple]) -> Tuple[ErrorInfo, DataFrame]:
    """
    根据券和账户查询持仓
    @param security_account_list:  券和账户的元组构成的列表，如[("600570.XSHG",account_info)]
    @return: 错误信息，持仓dataframe的元组
    """
    return FunctionImpl.get_position(security_account_list=security_account_list)


def get_security_base_info(security_list: list[str]) -> Tuple[ErrorInfo, Dict[str, SecurityBaseInfo]]:
    """
    获取证券的基础信息
    @param security_list: 券的列表，如["600570.XSHG","600000.XSHG"]
    @return: 错误信息，键为券值为证券基础信息的字典
    """
    return FunctionImpl.get_security_base_info(security_list=security_list)


def get_stock_base_info(security_list: list[str]) -> Tuple[ErrorInfo, Dict[str, StockBaseInfo]]:
    """
    获取证券的基础信息
    @param security_list: 券的列表，如["600570.XSHG","600000.XSHG"]
    @return: 错误信息，键为券值为现货基础信息的字典
    """
    return FunctionImpl.get_stock_base_info(security_list=security_list)


def get_bond_base_info(security_list: list[str]) -> Tuple[ErrorInfo, Dict[str, BondBaseInfo]]:
    """
    获取证券的基础信息
    @param security_list: 券的列表，如["600570.XSHG","600000.XSHG"]
    @return: 错误信息，键为券值为债券基础信息的字典
    """
    return FunctionImpl.get_bond_base_info(security_list=security_list)


def get_futures_base_info(security_list: list[str]) -> Tuple[ErrorInfo, Dict[str, FuturesBaseInfo]]:
    """
    获取证券的基础信息
    @param security_list: 券的列表，如["600570.XSHG","600000.XSHG"]
    @return: 错误信息，键为券值为期货基础信息的字典
    """
    return FunctionImpl.get_futures_base_info(security_list=security_list)


def get_option_base_info(security_list: list[str]) -> Tuple[ErrorInfo, Dict[str, OptionBaseInfo]]:
    """
    获取证券的基础信息
    @param security_list: 券的列表，如["600570.XSHG","600000.XSHG"]
    @return: 错误信息，键为券值为期权基础信息的字典
    """
    return FunctionImpl.get_option_base_info(security_list=security_list)


def get_etf_info(security: str) -> Tuple[ErrorInfo, ETFInfo]:
    """
    获取证券的基础信息
    @param security: 券，如"600570.XSHG"
    @return: 错误信息，键为券值为ETF申赎信息
    """
    return FunctionImpl.get_etf_info(security=security)


def get_etf_constituents(security: str) -> Tuple[ErrorInfo, DataFrame]:
    """
    获取ETF成分股信息
    @param security:券，如"600570.XSHG"
    @return:错误信息，ETF成分股信息
    """

    return FunctionImpl.get_etf_constituents(security=security)


def get_trades(security_account: Tuple) -> Tuple[ErrorInfo, DataFrame]:
    """
    获取账户成交流水
    @param security_account: 券和账户的元组构，如("600570.XSHG",account_info)
    @return:错误信息，成交数据dataframe的元组
    """
    return FunctionImpl.get_trades(security_account=security_account)


def get_open_orders(security_account: Tuple) -> Tuple[ErrorInfo, DataFrame]:
    """
    获取账户挂单委托
    @param security_account: 券和账户的元组构，如("600570.XSHG",account_info)
    @return:错误信息，挂单委托dataframe的元组
    """
    return FunctionImpl.get_open_orders(security_account=security_account)


def get_account_fund(account_info: AccountInfo, type: AccountType = None) -> Tuple[ErrorInfo, AccountFund]:
    """
    获取资金账户
    @param account_info:账户信息
    @param type:账户类型,None则表示两种类型都查
    @return:错误信息，账户资金信息的元组
    """
    return FunctionImpl.get_account_fund(account_info=account_info, type=type)


def get_factor(security_list: list[str], factor_name: str) -> Tuple[ErrorInfo, List[Factor]]:
    """
    快照行情查询
    @param security_list: 券的列表，如["600570.XSHG","600000.XSHG"]
    @param factor_name:因子名称
    @return:错误信息，因子信息列表的元组
    """
    return FunctionImpl.get_factor(security_list=security_list, factor_name=factor_name)


def get_chinabond_valuation(security_list: list[str], is_exercise: bool) -> Tuple[ErrorInfo, DataFrame]:
    """
    获取中债估值
    @param security_list:券的列表，如["600570.XSHG","600000.XSHG"]
    @param is_exercise: 是否行权，True为行权，yield=ytc; False为不行权, yield=ytm
    @return:错误信息，中债估值DataFrame
    """
    return FunctionImpl.get_chinabond_valuation(security_list=security_list, is_exercise=is_exercise)


def bond_pricing_calc(bond_valuation_list: list[BondCalcData]) -> Tuple[ErrorInfo, list[BondCalcData]]:
    """
    债券定价器
    @param bond_valuation_list:BondCalcData债券价格类 net_price ytm ytc 三者填一个
    @return:错误信息，债券价格列表
    """
    return FunctionImpl.bond_pricing_calc(bond_valuation_list=bond_valuation_list)

def get_historical_position(security_account_list: List[Tuple], days : int=0,start_date:int =0,end_date:int=0) -> Tuple[ErrorInfo, DataFrame]:
    """
    查询历史持仓
    @param security_account_list: 券和账户的元组构成的列表，如[("600570.XSHG",account_info)]
    @param days:交易日天数
    @return:错误信息，持仓数据DataFrame
    """
    return FunctionImpl.get_historical_position(security_account_list=security_account_list, days=days,start_date=start_date,end_date=end_date)



