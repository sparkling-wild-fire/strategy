# -*- coding: utf-8 -*-
import datetime
from typing import List, Tuple, Dict

from pandas import DataFrame

from qt_strategy_base import feq
from qt_strategy_base.core.cache.bond_hq_cache_manage import BondHQCacheManageBase
from qt_strategy_base.core.cache.bond_price_calc_manage import BondPriceCalcManage
from qt_strategy_base.core.cache.factor_cache_manage import FactorCacheManageBase
from qt_strategy_base.core.cache.global_params import GlobalParams
from qt_strategy_base.core.cache.hq_cache_manage import HQCacheManage
from qt_strategy_base.core.cache.intrabak_bond_hq_manage import IntrabakBondHqManage
from qt_strategy_base.core.cache.xbond_hq_cache_manage import XBondHQCacheManageBase
from qt_strategy_base.core.common import python_logger
from qt_strategy_base.core.common.constant import FunctionID
from qt_strategy_base.core.common.dict_covert_to_model import covert_message_to_class_list_tuple, \
    covert_message_to_class_dict_tuple, covert_message_to_dataframe_tuple, \
    covert_message_to_class_tuple, covert_message_to_dict_tuple, covert_csv_to_dataframe_tuple, \
    covert_message_to_p_class_list_tuple, covert_message_to_p_class_tuple
from qt_strategy_base.core.common.public_func import covert_to_enum
from qt_strategy_base.core.common.request import make_request, make_request2, make_request_no_recv
from qt_strategy_base.core.model.model import PStockBaseInfo, PETFInfo, POptionBaseInfo, \
    PFuturesBaseInfo, PBondBaseInfo, PSnapshotData, PNeeqSnapshotData, PFactor, PAccountFund, PAlgoStrategy, \
    PAlgoStrategyParamInfo, PQDBJHqInfo, PCJHqInfo, PBondPricing
from qt_strategy_base.core.scheme.algo_scheme_imp import AlgoSchemeImpl
from qt_strategy_base.model.enum import AdjustType, AccountType, Side, Direction, CloseType, OrderStatus, InvestType, \
    PositionType, ControlType, ClearSpeed
from qt_strategy_base.model.error_info import ErrorInfo
from qt_strategy_base.model.strategy_api_data import SecurityBaseInfo, AccountInfo, StockBaseInfo, BondBaseInfo, \
    FuturesBaseInfo, OptionBaseInfo, ETFInfo, SnapshotData, NeeqSnapshotData, Factor, AccountFund, BondClickHq, \
    BondQDBJInfo, BondCalcData


class FunctionImpl:
    @staticmethod
    def sub_snapshot(security_list: List[str]) -> ErrorInfo:
        error_info = ErrorInfo()
        fields: List[str] = ["security"]
        data: List[list] = [[x] for x in security_list]

        result_msg = make_request(function_id=FunctionID.SubHqBatch, fields=fields,
                                  data=data)
        error_info.set_value(result_msg['error_no'], result_msg['error_msg'])
        scheme_id = GlobalParams().current_scheme_id
        if error_info.has_error():
            python_logger.error(f"方案[{scheme_id}],{security_list}行情订阅失败")
        else:
            for security in security_list:
                HQCacheManage().add_or_update_subscribe_by_itemkey(item_key=security, scheme_id=scheme_id)
            python_logger.error(f"方案[{scheme_id}],{security_list}行情订阅成功")
        return error_info

    @staticmethod
    def sub_position(security_account_list: List[Tuple]) -> ErrorInfo:
        error_info = ErrorInfo()
        fields: List[str] = ["security", "investunit_id", "instance_id", "invest_type"]
        data: List[list] = []
        for stock_and_account in security_account_list:
            if len(stock_and_account) == 2 and isinstance(stock_and_account[0], str) and isinstance(
                    stock_and_account[1], AccountInfo):
                security = stock_and_account[0]
                account: AccountInfo = stock_and_account[1]
                data.append([security, account.investunit_id, account.portfolio_id, account.invest_type.value])
            else:
                error_info.set_error_value(error_msg="入参格式错误")
                return error_info

        result_msg = make_request(function_id=FunctionID.AddHoldSub, fields=fields,
                                  data=data)

        error_info.set_value(result_msg['error_no'], result_msg['error_msg'])
        return error_info

    @staticmethod
    def sub_order(security_account_list: List[Tuple]) -> ErrorInfo:
        error_info = ErrorInfo()
        fields: List[str] = ["security", "investunit_id", "instance_id", "invest_type"]
        data: List[list] = []
        for stock_and_account in security_account_list:
            if len(stock_and_account) == 2 and isinstance(stock_and_account[0], str) and isinstance(
                    stock_and_account[1], AccountInfo):
                security = stock_and_account[0]
                account: AccountInfo = stock_and_account[1]
                data.append([security, account.investunit_id, account.portfolio_id, account.invest_type.value])
            else:
                error_info.set_error_value(error_msg="入参格式错误")
                return error_info

        result_msg = make_request(function_id=FunctionID.AddEntrustSub, fields=fields,
                                  data=data)

        error_info.set_value(result_msg['error_no'], result_msg['error_msg'])
        return error_info

    @staticmethod
    def sub_trade(security_account_list: List[Tuple]) -> ErrorInfo:
        error_info = ErrorInfo()
        fields: List[str] = ["security", "investunit_id", "instance_id", "invest_type"]
        data: List[list] = []
        for stock_and_account in security_account_list:
            if len(stock_and_account) == 2 and isinstance(stock_and_account[0], str) and isinstance(
                    stock_and_account[1], AccountInfo):
                security = stock_and_account[0]
                account: AccountInfo = stock_and_account[1]
                data.append([security, account.investunit_id, account.portfolio_id, account.invest_type.value])
            else:
                error_info.set_error_value(error_msg="入参格式错误")
                return error_info

        result_msg = make_request(function_id=FunctionID.AddDealSub, fields=fields,
                                  data=data)

        error_info.set_value(result_msg['error_no'], result_msg['error_msg'])
        return error_info

    @staticmethod
    def sub_comb_order(security_account_list: List[Tuple]) -> ErrorInfo:
        error_info = ErrorInfo()
        fields: List[str] = ["security", "investunit_id", "instance_id", "invest_type"]
        data: List[list] = []
        for stock_and_account in security_account_list:
            if len(stock_and_account) == 2 and isinstance(stock_and_account[0], str) and isinstance(
                    stock_and_account[1], AccountInfo):
                security = stock_and_account[0]
                account: AccountInfo = stock_and_account[1]
                data.append([security, account.investunit_id, account.portfolio_id, account.invest_type.value])
            else:
                error_info.set_error_value(error_msg="入参格式错误")
                return error_info

        result_msg = make_request(function_id=FunctionID.AddCbEntrustSub, fields=fields,
                                  data=data)

        error_info.set_value(result_msg['error_no'], result_msg['error_msg'])
        return error_info

    @staticmethod
    def sub_market_duty(security_list: list[str]) -> ErrorInfo:
        error_info = ErrorInfo()
        fields: List[str] = ["security"]
        data: List[list] = [[x] for x in security_list]
        result_msg = make_request(function_id=FunctionID.AddMktDutySub, fields=fields,
                                  data=data)
        error_info.set_value(result_msg['error_no'], result_msg['error_msg'])
        return error_info

    @staticmethod
    def sub_factor(security_list: list[str], factor: str) -> ErrorInfo:
        error_info = ErrorInfo()
        fields: List[str] = ["security", "factor"]
        data: List[list] = []
        for security in security_list:
            data.append([security, factor])
        result_msg = make_request(function_id=FunctionID.SubFactor, fields=fields,
                                  data=data)
        error_info.set_value(result_msg['error_no'], result_msg['error_msg'])
        scheme_id = GlobalParams().current_scheme_id
        if error_info.has_error():
            python_logger.error(f"方案[{scheme_id}],{security_list},{factor}因子订阅失败")
        else:
            for security in security_list:
                FactorCacheManageBase().add_or_update_subscribe_by_itemkey(item_key=f"{security},{factor}",
                                                                           scheme_id=scheme_id)
            python_logger.error(f"方案[{scheme_id}],{security_list},{factor}因子订阅成功")
        return error_info

    @staticmethod
    def bond_click_hq(security_list: list[str], clear_speed: ClearSpeed = None) -> ErrorInfo:
        error_info = ErrorInfo()
        scheme_id = GlobalParams().current_scheme_id
        fields: List[str] = ["security", "clear_speed"]
        data: List[list] = []
        for security in security_list:
            security_arr = security.split('.')
            if len(security_arr) != 2:
                error_info.set_error_value(f"{security}格式错误")
                return error_info
            else:
                if security_arr[1] == "XSHG":
                    if clear_speed is not None:
                        error_info.set_error_value(f"{security}上交所clear_speed必须是None")
                        return error_info
                elif security_arr[1] == "XSHE":
                    if clear_speed != ClearSpeed.TP1 or clear_speed != ClearSpeed.TP0:
                        error_info.set_error_value(f"{security}深交所clear_speed必须是T1或T0")
                        return error_info
                else:
                    error_info.set_error_value(f"{security}市场错误")
                    return error_info
        clear_speed_value = -1 if clear_speed is None else clear_speed.value
        bond_hq_cache_manage_base: BondHQCacheManageBase = BondHQCacheManageBase()
        fail_security_list = []
        for security in security_list:
            data.clear()
            data.append([security, clear_speed_value])
            qdbj_result_msg = make_request(function_id=FunctionID.SubQDBJHq, fields=fields,
                                           data=data)
            qdbj_error_info = ErrorInfo()
            qdbj_error_info.set_value(qdbj_result_msg['error_no'], qdbj_result_msg['error_msg'])
            if not qdbj_error_info.has_error():
                cj_error_info = ErrorInfo()
                cj_result_msg = make_request(function_id=FunctionID.SubCJHq, fields=fields,
                                             data=data)
                cj_error_info.set_value(cj_result_msg['error_no'], cj_result_msg['error_msg'])
                if cj_error_info.has_error():
                    fail_security_list.append(security)
                else:
                    bond_hq_cache_manage_base.add_bond_click_subscribe_by_itemkey(
                        item_key=f"{security},{clear_speed_value}",
                        scheme_id=scheme_id)
            else:
                fail_security_list.append(security)
        if len(fail_security_list) != 0:
            fail_security = ",".join(fail_security_list)
            error_info.set_error_value(f"点击成交行情部分失败，失败券为{fail_security}")
            python_logger.error(error_info.error_msg)
        return error_info

    @staticmethod
    def sub_xbond(security_list: list[str], clear_speed: ClearSpeed = None) -> ErrorInfo:
        error_info = ErrorInfo()
        fields: List[str] = ["security", "clear_speed"]
        data: List[list] = []
        clear_speed_value = -1 if clear_speed is None else clear_speed.value
        for security in security_list:
            data = [[security, clear_speed_value]]
            result_msg = make_request(function_id=FunctionID.SubXBondHq, fields=fields,
                                      data=data)
            error_info.set_value(result_msg['error_no'], result_msg['error_msg'])
            scheme_id = GlobalParams().current_scheme_id
            if error_info.has_error():
                python_logger.error(f"方案[{scheme_id}],{security_list}行情订阅失败")
            else:
                XBondHQCacheManageBase().add_or_update_subscribe_by_itemkey(item_key=f"{security},{clear_speed_value}",
                                                                            scheme_id=scheme_id)
                python_logger.error(f"方案[{scheme_id}],{security_list}行情订阅成功")
            return error_info

    @staticmethod
    def sub_intrabak_bond_mm(security_list: list[str], clear_speed: ClearSpeed = None) -> ErrorInfo:
        error_info = ErrorInfo()
        fields: List[str] = ["security", "clear_speed"]
        data: List[list] = []
        clear_speed_value = -1 if clear_speed is None else clear_speed.value
        for security in security_list:
            data = [[security, clear_speed_value]]
            result_msg = make_request(function_id=FunctionID.SubIntrabakBondMM, fields=fields,
                                      data=data)
            error_info.set_value(result_msg['error_no'], result_msg['error_msg'])
            scheme_id = GlobalParams().current_scheme_id
            if error_info.has_error():
                python_logger.error(f"方案[{scheme_id}],{security_list}行情订阅失败")
            else:
                IntrabakBondHqManage().add_or_update_subscribe_by_itemkey(item_key=f"{security},{clear_speed_value}",
                                                                          scheme_id=scheme_id)
                python_logger.error(f"方案[{scheme_id}],{security_list}行情订阅成功")
            return error_info

    @staticmethod
    def unsub_snapshot() -> ErrorInfo:
        """
        取消行情订阅
        @return: 错误信息
        """
        error_info = ErrorInfo()
        scheme_id = GlobalParams().current_scheme_id
        unsubscribe_list = HQCacheManage().get_un_subscribe_list_by_scheme_id(scheme_id=scheme_id)
        if len(unsubscribe_list) == 0:
            return error_info
        fields: List[str] = ['security']
        data: List[list] = [[x] for x in unsubscribe_list]
        result_msg = make_request(function_id=FunctionID.UnSubscribeHQ, fields=fields,
                                  data=data)
        error_info.set_value(result_msg['error_no'], result_msg['error_msg'])
        if error_info.has_error():
            for item_key in unsubscribe_list:
                HQCacheManage().add_or_update_subscribe_by_itemkey(item_key=item_key, scheme_id=scheme_id)
        return error_info

    @staticmethod
    def unsub_position() -> ErrorInfo:
        """
        取消持仓订阅
        @return:错误信息
        """
        error_info = ErrorInfo()
        fields: List[str] = []
        data: List[list] = [[]]
        result_msg = make_request(function_id=FunctionID.ReleaseHoldSub, fields=fields,
                                  data=data)
        error_info.set_value(result_msg['error_no'], result_msg['error_msg'])
        return error_info

    @staticmethod
    def unsub_order() -> ErrorInfo:
        """
        取消委托订阅
        @return:错误信息
        """

        error_info = ErrorInfo()
        fields: List[str] = []
        data: List[list] = [[]]
        result_msg = make_request(function_id=FunctionID.ReleaseEntrustSub, fields=fields,
                                  data=data)
        error_info.set_value(result_msg['error_no'], result_msg['error_msg'])
        return error_info

    @staticmethod
    def unsub_trade() -> ErrorInfo:
        """
        取消成交订阅
        @return:错误信息
        """
        error_info = ErrorInfo()
        fields: List[str] = []
        data: List[list] = [[]]
        result_msg = make_request(function_id=FunctionID.ReleaseDealSub, fields=fields,
                                  data=data)
        error_info.set_value(result_msg['error_no'], result_msg['error_msg'])
        return error_info

    @staticmethod
    def unsub_comb_order() -> ErrorInfo:
        """
        取消合笔委托订阅
        @return:错误信息
        """

        error_info = ErrorInfo()
        fields: List[str] = []
        data: List[list] = [[]]
        result_msg = make_request(function_id=FunctionID.ReleaseCbEntrustSub, fields=fields,
                                  data=data)
        error_info.set_value(result_msg['error_no'], result_msg['error_msg'])
        return error_info

    @staticmethod
    def unsub_market_duty() -> ErrorInfo:
        """
        取消做市义务订阅
        @return:错误信息
        """
        error_info = ErrorInfo()
        fields: List[str] = []
        data: List[list] = [[]]
        result_msg = make_request(function_id=FunctionID.ReleaseMktDutySub, fields=fields,
                                  data=data)
        error_info.set_value(result_msg['error_no'], result_msg['error_msg'])
        return error_info

    @staticmethod
    def unsub_factor() -> ErrorInfo:
        """
        取消因子订阅
        @return:错误信息
        """
        error_info = ErrorInfo()
        scheme_id = GlobalParams().current_scheme_id
        unsubscribe_list = FactorCacheManageBase().get_un_subscribe_list_by_scheme_id(scheme_id=scheme_id)
        if len(unsubscribe_list) == 0:
            return error_info
        fields: List[str] = ["security", "factor"]
        data: List[list] = []
        for item in unsubscribe_list:
            security, factor = item.split(',')
            data.append([security, factor])
        result_msg = make_request(function_id=FunctionID.UnSubFactor, fields=fields,
                                  data=data)
        error_info.set_value(result_msg['error_no'], result_msg['error_msg'])
        if error_info.has_error():
            for item_key in unsubscribe_list:
                FactorCacheManageBase().add_or_update_subscribe_by_itemkey(item_key=item_key, scheme_id=scheme_id)
        return error_info

    @staticmethod
    def unsub_bond_click_hq() -> ErrorInfo:
        """
        取消债券点击行情订阅
        @return: 错误信息
        """
        error_info = ErrorInfo()
        scheme_id = GlobalParams().current_scheme_id
        unsubscribe_list = BondHQCacheManageBase().get_unsubscribe_list_by_scheme_id(scheme_id=scheme_id)
        if len(unsubscribe_list) == 0:
            return error_info
        fields: List[str] = ["security", "clear_speed"]
        data: List[list] = []
        for sub_key in unsubscribe_list:
            security, clear_speed = sub_key.split(",")
            data = [[security, clear_speed]]
            make_request_no_recv(scheme_id=scheme_id, function_id=FunctionID.UnSubCJHq, fields=fields,
                                 data=data)
            make_request_no_recv(scheme_id=scheme_id, function_id=FunctionID.UnSubQDBJHq, fields=fields,
                                 data=data)
        return error_info

    @staticmethod
    def unsub_xbond() -> ErrorInfo:
        """
        取消xbond订阅
        @return: 错误信息
        """
        error_info = ErrorInfo()
        scheme_id = GlobalParams().current_scheme_id
        unsubscribe_list = XBondHQCacheManageBase().get_un_subscribe_list_by_scheme_id(scheme_id=scheme_id)
        if len(unsubscribe_list) == 0:
            return error_info
        fields: List[str] = ['security', "clear_speed"]
        data: List[list] = []
        for sub_key in unsubscribe_list:
            security, clear_speed = sub_key.split(",")
            data = [[security, clear_speed]]
            result_msg = make_request_no_recv(scheme_id=scheme_id, function_id=FunctionID.UnSubscribeXBondHQ,
                                              fields=fields, data=data)
        return error_info

    @staticmethod
    def unsub_intrabank_bond_mm() -> ErrorInfo:
        """
        取消银行间做市行情订阅
        @return: 错误信息
        """
        error_info = ErrorInfo()
        scheme_id = GlobalParams().current_scheme_id
        unsubscribe_list = IntrabakBondHqManage().get_un_subscribe_list_by_scheme_id(scheme_id=scheme_id)
        if len(unsubscribe_list) == 0:
            return error_info
        fields: List[str] = ['security', "clear_speed"]
        data: List[list] = []
        for sub_key in unsubscribe_list:
            security, clear_speed = sub_key.split(",")
            data = [[security, clear_speed]]
            result_msg = make_request_no_recv(scheme_id=scheme_id, function_id=FunctionID.UnSubIntrabakBondMM,
                                              fields=fields,
                                              data=data)
        return error_info

    @staticmethod
    def get_section_no() -> Tuple[ErrorInfo, dict]:
        fields: List[str] = [""]
        data: List[list] = [[]]
        result_dict = make_request(FunctionID.GetOrderIdStart, fields, data)
        error_info, data_dict = covert_message_to_dict_tuple(msg=result_dict, data_name="info")
        return error_info, data_dict

    @staticmethod
    def get_position(security_account_list: List[Tuple]) -> Tuple[ErrorInfo, DataFrame]:
        error_info: ErrorInfo = ErrorInfo()
        fields: List[str] = ["security", "investunit_id", "instance_id", "invest_type"]
        data: List[list] = []
        for stock_and_account in security_account_list:
            if len(stock_and_account) == 2 and isinstance(stock_and_account[0], str) and isinstance(
                    stock_and_account[1], AccountInfo):
                security = stock_and_account[0]
                account: AccountInfo = stock_and_account[1]
                data.append([security, account.investunit_id, account.portfolio_id, account.invest_type.value])
            else:
                error_info.set_error_value(error_msg="入参格式错误")
                return error_info, None

        result_dict = make_request(function_id=FunctionID.GetHoldList, fields=fields, data=data)
        converters = {
            "security": str,  # 代码
            "invest_type": int,  # 投资类型
            "position_type": int,  # 多空类型
            "initial_position": float,  # 期初数量
            "position": float,  # 当前持仓数量
            "available_position": float,  # 可用数量
            "yesterday_available_position": float,  # 昨仓可用数量
            "today_available_position": float,  # 今仓可用
            "buy_volume": float,  # 当日买成交数量
            "buy_value": float,  # 当日买成交金额
            "sell_volume": float,  # 当日卖成交数量
            "sell_value": float,  # 当日卖成交金额
            "unfilled_order_buy_quantity": float,  # 买挂单数量
            "unfilled_order_sell_quantity": float,  # 卖挂单数量
            "frozen_quantity": float,  # 冻结数量
            "cost": float,  # 持仓成本
            "total_fee": float,  # 持仓费用
            "investunit_id": int,  # 账户 ID
            "portfolio_id": int,  # 投资组合 ID
            "etf_purchase_quantity": float,  # etf申购成交数量
            "etf_redeem_quantity": float,  # etf赎回成交数量

        }
        error_info, data_dataframe = covert_csv_to_dataframe_tuple(msg=result_dict, converters=converters)
        data_dataframe['position_type'] = data_dataframe['position_type'].apply(
            lambda x: covert_to_enum(x, PositionType))
        data_dataframe['invest_type'] = data_dataframe['invest_type'].apply(lambda x: covert_to_enum(x, InvestType))
        return error_info, data_dataframe

    @staticmethod
    def get_security_base_info(security_list: List[str]) -> Tuple[ErrorInfo, Dict[str, SecurityBaseInfo]]:
        fields: List[str] = ["security"]
        data: List[list] = [[x] for x in security_list]
        result_dict = make_request(function_id=FunctionID.GetStockInfo, fields=fields, data=data)
        error_info, result_data = covert_message_to_class_dict_tuple(msg=result_dict, data_name="info",
                                                                     data_class=PStockBaseInfo,
                                                                     return_class=SecurityBaseInfo)

        return error_info, result_data

    @staticmethod
    def get_stock_base_info(security_list: list[str]) -> Tuple[ErrorInfo, Dict[str, StockBaseInfo]]:
        fields: List[str] = ["security"]
        data: List[list] = [[x] for x in security_list]
        result_dict = make_request(function_id=FunctionID.GetStockInfo, fields=fields, data=data)
        error_info, result_data = covert_message_to_class_dict_tuple(msg=result_dict, data_name="info",
                                                                     data_class=PStockBaseInfo,
                                                                     return_class=StockBaseInfo)

        return error_info, result_data

    @staticmethod
    def get_bond_base_info(security_list: list[str]) -> Tuple[ErrorInfo, Dict[str, BondBaseInfo]]:
        fields: List[str] = ["security"]
        data: List[list] = [[x] for x in security_list]
        result_dict = make_request(function_id=FunctionID.GetBondProperty, fields=fields, data=data)
        error_info, result_data = covert_message_to_class_dict_tuple(msg=result_dict, data_name="info",
                                                                     data_class=PBondBaseInfo,
                                                                     return_class=BondBaseInfo)

        return error_info, result_data

    @staticmethod
    def get_futures_base_info(security_list: list[str]) -> Tuple[ErrorInfo, Dict[str, FuturesBaseInfo]]:
        fields: List[str] = ["security"]
        data: List[list] = [[x] for x in security_list]
        result_dict = make_request(function_id=FunctionID.GetFutureInfo, fields=fields, data=data)
        error_info, result_data = covert_message_to_class_dict_tuple(msg=result_dict, data_name="info",
                                                                     data_class=PFuturesBaseInfo,
                                                                     return_class=FuturesBaseInfo)

        return error_info, result_data

    @staticmethod
    def get_option_base_info(security_list: list[str]) -> Tuple[ErrorInfo, Dict[str, OptionBaseInfo]]:
        fields: List[str] = ["security"]
        data: List[list] = [[x] for x in security_list]
        result_dict = make_request(function_id=FunctionID.GetOptionInfo, fields=fields, data=data)
        error_info, result_data = covert_message_to_class_dict_tuple(msg=result_dict, data_name="info",
                                                                     data_class=POptionBaseInfo,
                                                                     return_class=OptionBaseInfo)

        return error_info, result_data

    @staticmethod
    def get_etf_info(security: str) -> Tuple[ErrorInfo, ETFInfo]:
        fields: List[str] = ["security"]
        data: List[list] = [[security]]
        result_dict = make_request(function_id=FunctionID.GetEtfInfo, fields=fields, data=data)
        error_info, result_data = covert_message_to_class_tuple(msg=result_dict, data_name="info",
                                                                data_class=PETFInfo,
                                                                return_class=ETFInfo)

        return error_info, result_data

    @staticmethod
    def get_etf_constituents(security: str) -> Tuple[ErrorInfo, DataFrame]:
        fields: List[str] = ["security"]
        data: List[list] = [[security]]
        result_dict = make_request(function_id=FunctionID.GetEtfStocks, fields=fields, data=data)
        error_info, result_data = covert_message_to_dataframe_tuple(msg=result_dict, data_name="info")

        return error_info, result_data

    @staticmethod
    def get_snapshot(security_list: list[str]) -> Tuple[ErrorInfo, Dict[str, SnapshotData]]:
        fields: List[str] = ["security"]
        data: List[list] = [[x] for x in security_list]
        msg = make_request(function_id=FunctionID.GetHqBatch, fields=fields, data=data)

        return covert_message_to_class_dict_tuple(msg=msg, data_name="hq_infos", data_class=PSnapshotData,
                                                  return_class=SnapshotData)

    '''
    @staticmethod
    def get_snapshot(security_list: list[str]) -> Tuple[ErrorInfo, List[SnapshotData]]:
        error_info = ErrorInfo()
        hq_cache_manage_base: HQCacheManageBase = HQCacheManageBase()
        hq_result = []
        query_list = []
        for security in security_list:
            hq = hq_cache_manage_base.query_hq_by_itemkey(item_key=security)
            if hq is not None:
                hq_result.append(hq)
            else:
                query_list.append(security)
        if len(query_list) > 0:
            fields: List[str] = ["security"]
            data: List[list] = [[x] for x in query_list]
            msg = make_request(function_id=FunctionID.GetHqBatch, fields=fields, data=data)
            error_info, query_result_list = covert_message_to_class_list_tuple(msg=msg, data_name="hq_infos",
                                                                               data_class=PSnapshotData,
                                                                               return_class=SnapshotData)
            hq_result.extend(query_result_list)

        return error_info, hq_result
    '''

    @staticmethod
    def get_neeq_snapshot(security_list: list[str]) -> Tuple[ErrorInfo, Dict[str, NeeqSnapshotData]]:
        fields: List[str] = ["security"]
        data: List[list] = [[x] for x in security_list]
        msg = make_request(function_id=FunctionID.GetNEEQHq, fields=fields, data=data)

        return covert_message_to_class_dict_tuple(msg=msg, data_name="info", data_class=PNeeqSnapshotData,
                                                  return_class=NeeqSnapshotData)

    @staticmethod
    def get_bond_click_snapshot(security_list: list[str], clear_speed: ClearSpeed = None) -> Tuple[
        ErrorInfo, List[BondClickHq]]:
        error_info = ErrorInfo()
        hq_cache_manage_base: BondHQCacheManageBase = BondHQCacheManageBase()
        clear_speed_value = -1 if clear_speed is None else clear_speed.value
        hq_result = []
        query_list = []
        for security in security_list:
            sub_key = f"{security},{clear_speed_value}"
            cj_hq = hq_cache_manage_base.query_cj_hq_by_itemkey(item_key=sub_key)
            qdbj_hq = hq_cache_manage_base.query_qdbj_hq_by_itemkey(item_key=sub_key)
            if cj_hq is not None and qdbj_hq is not None:
                bond_click_hq = BondClickHq(qdbj_data_info=qdbj_hq, cj_data_info=cj_hq)
                hq_result.append(bond_click_hq)
            else:
                query_list.append(security)

        for query_item in query_list:
            fields: List[str] = ["security", "cleae_speed"]
            data: List[list] = [[query_item, clear_speed_value]]
            cj_hq_msg = make_request(function_id=FunctionID.GetCJHq, fields=fields, data=data)
            qdbj_hq_msg = make_request(function_id=FunctionID.GetQDBJHq, fields=fields, data=data)
            error_info, cj_hq = covert_message_to_p_class_tuple(msg=cj_hq_msg['msg_content'], data_name="info",
                                                                data_class=PCJHqInfo)
            buy_hq_info_list = []
            sell_hq_info_list = []
            if "buy_info" in qdbj_hq_msg['msg_content']['body'].keys():
                error_info, buy_hq_info_list_result = covert_message_to_class_list_tuple(msg=qdbj_hq_msg['msg_content'],
                                                                                         data_name="buy_info",
                                                                                         data_class=PQDBJHqInfo,
                                                                                         return_class=BondQDBJInfo)
                if not error_info.has_error():
                    buy_hq_info_list = buy_hq_info_list_result
            if "sale_info" in qdbj_hq_msg['msg_content']['body'].keys():
                error_info, sell_hq_info_list_result = covert_message_to_class_list_tuple(
                    msg=qdbj_hq_msg['msg_content'],
                    data_name="sale_info",
                    data_class=PQDBJHqInfo,
                    return_class=BondQDBJInfo)
                if not error_info.has_error():
                    sell_hq_info_list = sell_hq_info_list_result
            qdbj_hq = {"buy_info": buy_hq_info_list, "sale_info": sell_hq_info_list}
            bond_click_hq = BondClickHq(qdbj_data_info=qdbj_hq, cj_data_info=cj_hq)
            hq_result.append(bond_click_hq)
        return error_info, hq_result

    @staticmethod
    def get_history_kline(security_list: list[str], start_time: str, end_time: str, count: int, frequency: str,
                          fields: str, adjust_type: AdjustType) -> DataFrame:
        pass

    @staticmethod
    def get_factor(security_list: list[str], factor_name: str) -> Tuple[ErrorInfo, List[Factor]]:
        fields: List[str] = ["security", "factor"]
        data: List[list] = []
        for security in security_list:
            data.append([security, factor_name])
        msg = make_request(function_id=FunctionID.GetFactor, fields=fields, data=data)

        return covert_message_to_class_list_tuple(msg=msg, data_name="info", data_class=PFactor,
                                                  return_class=Factor)

    @staticmethod
    def get_trades(security_account: Tuple) -> Tuple[ErrorInfo, DataFrame]:
        error_info: ErrorInfo = ErrorInfo()
        fields: List[str] = ["security", "investunit_id", "instance_id"]
        data: List[list] = []

        if len(security_account) == 2 and isinstance(security_account[0], str) and isinstance(
                security_account[1], AccountInfo):
            security = security_account[0]
            account: AccountInfo = security_account[1]
            data.append([security, account.investunit_id, account.portfolio_id])
        else:
            error_info.set_error_value(error_msg="入参格式错误")
            return error_info, None

        result_dict = make_request(function_id=FunctionID.GetTrades, fields=fields, data=data)
        converters = {
            "security": str,  # 代码
            "id": int,  # 成交编号
            "datetime": float,  # 成交时间
            "volume": float,  # 成交数量
            "value": float,  # 成交金额
            "order_quantity": float,  # 委托数量
            "side": int,  # 委托方向
            "direction": int,  # 开平方向
            "close_type": int,  # 平仓方向
            "internal_id": str,  # 内部委托号
            "order_id": int,  # 外部委托编号
            "invest_type": int,  # 投资类型
            "fee": float,  # 当次费用
            "remark": str,  # 备注
            "investunit_id": int,  # 账户 ID
            "portfolio_id": int,  # 投资组合 ID
            "scheme_id": int,  # 方案号
            "security_detail_id": str  # 方案明细号
        }

        error_info, data_dataframe = covert_csv_to_dataframe_tuple(msg=result_dict, converters=converters)
        data_dataframe['side'] = data_dataframe['side'].apply(lambda x: covert_to_enum(x, Side))
        data_dataframe['direction'] = data_dataframe['direction'].apply(lambda x: covert_to_enum(x, Direction))
        data_dataframe['close_type'] = data_dataframe['close_type'].apply(lambda x: covert_to_enum(x, CloseType))
        data_dataframe['invest_type'] = data_dataframe['invest_type'].apply(lambda x: covert_to_enum(x, InvestType))
        data_dataframe['datetime'] = data_dataframe['datetime'].apply(lambda x: datetime.datetime.fromtimestamp(x))
        return error_info, data_dataframe

    @staticmethod
    def get_open_orders(security_account: Tuple) -> Tuple[ErrorInfo, DataFrame]:
        error_info: ErrorInfo = ErrorInfo()
        fields: List[str] = ["security", "investunit_id", "instance_id"]
        data: List[list] = []

        if len(security_account) == 2 and isinstance(security_account[0], str) and isinstance(
                security_account[1], AccountInfo):
            security = security_account[0]
            account: AccountInfo = security_account[1]
            data.append([security, account.investunit_id, account.portfolio_id])
        else:
            error_info.set_error_value(error_msg="入参格式错误")
            return error_info, None

        result_dict = make_request(function_id=FunctionID.GetOpenOrders, fields=fields, data=data)
        converters = {
            "id": int,  # 委托编号
            "security": str,  # 代码
            "datetime": float,  # 委托时间
            "price": float,  # 委托价格
            "quantity": float,  # 委托数量
            "side": int,  # 委托方向
            "direction": int,  # 开平方向
            "close_type": int,  # 平仓类型
            "status": int,  # 委托状态
            "invest_type": int,  # 投资类型
            "internal_id": str,  # 内部委托号
            "revoke_cause": str,  # 委托拒绝/委托撤废等原因
            "cancel_value": float,  # 撤单数量
            "cancel_quantity": float,  # 撤单数量
            "investunit_id": int,  # 投资单元ID
            "portfolio_id": int,  # 投资组合 ID
            "filled_quantity": float,  # 成交数量
            "filled_value": float,  # 成交金额
            "remark": str,  # 备注
            "scheme_id": int,  # 方案号
            "security_detail_id": str,  # 方案明细号
            "operator_no": int  # 操作员号
        }
        error_info, data_dataframe = covert_csv_to_dataframe_tuple(msg=result_dict, converters=converters)
        data_dataframe = data_dataframe.drop(columns='cancel_value')
        data_dataframe['side'] = data_dataframe['side'].apply(lambda x: covert_to_enum(x, Side))
        data_dataframe['direction'] = data_dataframe['direction'].apply(lambda x: covert_to_enum(x, Direction))
        data_dataframe['close_type'] = data_dataframe['close_type'].apply(lambda x: covert_to_enum(x, CloseType))
        data_dataframe['status'] = data_dataframe['status'].apply(lambda x: covert_to_enum(x, OrderStatus))
        data_dataframe['invest_type'] = data_dataframe['invest_type'].apply(lambda x: covert_to_enum(x, InvestType))
        data_dataframe['datetime'] = data_dataframe['datetime'].apply(lambda x: datetime.datetime.fromtimestamp(x))
        return error_info, data_dataframe

    @staticmethod
    def get_account_fund(account_info: AccountInfo, type: AccountType = None) -> Tuple[ErrorInfo, AccountFund]:
        fields: List[str] = ["account_type", "investunit_id"]
        account_type = 0 if type is None else type.value
        data: List[list] = [
            [account_type, account_info.investunit_id, account_info.portfolio_id, account_info.invest_type.value]]
        msg = make_request(function_id=FunctionID.GetAccountFund, fields=fields, data=data)

        return covert_message_to_class_tuple(msg=msg, data_name="info", data_class=PAccountFund,
                                             return_class=AccountFund)

    @staticmethod
    def get_sub_scheme(strategy_id: int, control_type: ControlType) -> Tuple[ErrorInfo, AlgoSchemeImpl]:
        error_info = ErrorInfo()
        fields: List[str] = ["strategy_id", "control_type"]
        data: List[list] = [[strategy_id, control_type.value]]
        msg = make_request(function_id=FunctionID.GetAlgoScheme, fields=fields, data=data)

        error_info1, p_params_info = covert_message_to_p_class_list_tuple(msg=msg, data_name="param_info",
                                                                          data_class=PAlgoStrategyParamInfo)
        error_info2, p_algo_scheme = covert_message_to_p_class_tuple(msg=msg, data_name="strategy_info",
                                                                     data_class=PAlgoStrategy)
        if error_info1.has_error() or p_algo_scheme is None:
            error_info.set_error_value(error_msg="子方案信息错误！")
            python_logger.error(f"{strategy_id}策略创建方案失败，原因：子方案信息错误！")
            return error_info, None
        if error_info2.has_error() or len(p_params_info) == 0:
            python_logger.error(f"{strategy_id}策略创建方案失败，原因：策略信息错误！")
            return error_info, None
        params_info = {}
        strategy_params = {}
        for item in p_params_info:
            params_info[item.name] = item.type
            strategy_params[item.name] = ""
        algo_scheme = AlgoSchemeImpl(strategy_info=p_algo_scheme, params_info=params_info,
                                     strategy_params=strategy_params, control_type=control_type)
        return error_info, algo_scheme

    @staticmethod
    def run_algo_scheme(request_params: dict) -> Tuple[ErrorInfo, dict]:
        msg = make_request2(function_id=FunctionID.RunAlgoScheme, request_params=request_params)
        return covert_message_to_dict_tuple(msg=msg, data_name="info")

    @staticmethod
    def cancel_algo_scheme(algo_scheme_id: int) -> Tuple[ErrorInfo, dict]:
        fields: List[str] = ["scheme_id"]
        data: List[list] = [[algo_scheme_id]]
        msg = make_request(function_id=FunctionID.CancelAlgoScheme, fields=fields, data=data)
        return covert_message_to_dict_tuple(msg=msg, data_name="info")

    @staticmethod
    def get_chinabond_valuation(security_list: list[str], is_exercise: bool) -> Tuple[ErrorInfo, DataFrame]:
        error_info = ErrorInfo()
        fields: List[str] = ["security", "is_exercise"]
        data: List[list] = []
        is_exercise_value = 1 if is_exercise else 0
        for security in security_list:
            data.append([security, is_exercise_value])
        result_dict = make_request(function_id=FunctionID.GetChinabondValuation, fields=fields, data=data)
        converters = {
            "security": str,  # 委托编号
            "net_price": float,  # 代码
            "ytm": float,  # 委托时间
            "is_exercise": float,  # 委托价格
        }

        error_info, data_dataframe = covert_csv_to_dataframe_tuple(msg=result_dict, converters=converters)
        data_dataframe['is_exercise'] = data_dataframe['is_exercise'].apply(lambda x: True if x == 1 else False)
        return error_info, data_dataframe

    @staticmethod
    def bond_pricing_calc(bond_valuation_list: list[BondCalcData]) -> Tuple[ErrorInfo, list[BondCalcData]]:
        error_info = ErrorInfo()
        bond_price_calc_manage: BondPriceCalcManage = BondPriceCalcManage()
        fields: List[str] = ["security", "date", "full_price", "value", "type"]
        data: List[list] = []
        net_price_list = []
        ytm_list = []
        ytc_list = []
        bond_price_list = []
        for bond_valuation in bond_valuation_list:

            if not feq(bond_valuation.net_price, 0):
                net_price_list.append(bond_valuation)
            elif not feq(bond_valuation.ytm, 0):
                ytm_list.append(bond_valuation)
            elif not feq(bond_valuation.ytc, 0):
                ytc_list.append(bond_valuation)
        if len(net_price_list) > 0:
            for bond_valuation in net_price_list:
                target_data = int(bond_valuation.date)
                bond_price = bond_price_calc_manage.get_by_key(
                    f"{bond_valuation.security},{bond_valuation.date},{bond_valuation.net_price}", 1)
                if bond_price is not None:
                    bond_price_list.append(bond_price)
                else:
                    data.append(
                        [bond_valuation.security, target_data, bond_valuation.full_price,
                         bond_valuation.net_price, 1])
            if len(data) != 0:
                result_dict = make_request(function_id=FunctionID.BondPricingCalc, fields=fields, data=data)
                error_info, p_params_info = covert_message_to_p_class_list_tuple(msg=result_dict,
                                                                                 data_name="info",
                                                                                 data_class=PBondPricing)
                if error_info.has_error():
                    return error_info, []
                current_index = 0
                if p_params_info is not None:
                    for bond_price in p_params_info:
                        item = BondCalcData()
                        item.security = bond_price.security
                        item.date = bond_price.date
                        item.full_price = bond_price.full_price
                        item.net_price = bond_price.net_price
                        item.ytm = bond_price.ytm / 100
                        item.ytc = bond_price.ytc / 100
                        item.yield_error = bond_price.yield_error
                        bond_price_calc_manage.add_or_update(
                            price_key=f"{data[current_index][0]},{data[current_index][1]},{data[current_index][3]}",
                            key_type=1,
                            bond_price=bond_price)
                        bond_price_list.append(bond_price)
                        current_index = current_index + 1

        if len(ytm_list) > 0:
            data.clear()
            for bond_valuation in ytm_list:
                target_data = int(bond_valuation.date)
                bond_price = bond_price_calc_manage.get_by_key(
                    f"{bond_valuation.security},{bond_valuation.date},{bond_valuation.ytm}", 2)
                if bond_price is not None:
                    bond_price_list.append(bond_price)
                else:
                    data.append(
                        [bond_valuation.security, target_data, bond_valuation.full_price,
                         bond_valuation.ytm, 2])
            if len(data) != 0:
                result_dict = make_request(function_id=FunctionID.BondPricingCalc, fields=fields, data=data)
                error_info, p_params_info = covert_message_to_p_class_list_tuple(msg=result_dict,
                                                                                 data_name="info",
                                                                                 data_class=PBondPricing)
                if error_info.has_error():
                    return error_info, []
                current_index = 0
                if p_params_info is not None:
                    for bond_price in p_params_info:
                        item = BondCalcData()
                        item.security = bond_price.security
                        item.date = bond_price.date
                        item.full_price = bond_price.full_price
                        item.net_price = bond_price.net_price
                        item.ytm = bond_price.ytm / 100
                        item.ytc = bond_price.ytc / 100
                        item.yield_error = bond_price.yield_error
                        bond_price_calc_manage.add_or_update(
                            price_key=f"{data[current_index][0]},{data[current_index][1]},{data[current_index][3]}",
                            key_type=2,
                            bond_price=bond_price)
                        bond_price_list.append(bond_price)
                        current_index = current_index + 1
        if len(ytc_list) > 0:
            data.clear()
            for bond_valuation in ytc_list:
                target_data = int(bond_valuation.date)
                bond_price = bond_price_calc_manage.get_by_key(
                    f"{bond_valuation.security},{bond_valuation.date},{bond_valuation.ytc}", 3)
                if bond_price is not None:
                    bond_price_list.append(bond_price)
                else:
                    data.append(
                        [bond_valuation.security, target_data, bond_valuation.full_price, bond_valuation.ytc,
                         3])
                result_dict = make_request(function_id=FunctionID.BondPricingCalc, fields=fields, data=data)
                error_info, p_params_info = covert_message_to_p_class_list_tuple(msg=result_dict,
                                                                                 data_name="info",
                                                                                 data_class=PBondPricing)
                if error_info.has_error():
                    return error_info, []
                if len(data) != 0:
                    current_index = 0
                    if p_params_info is not None:
                        for bond_price in p_params_info:
                            item: BondCalcData = BondCalcData()
                            item.security = bond_price.security
                            item.date = bond_price.date
                            item.full_price = bond_price.full_price
                            item.net_price = bond_price.net_price
                            item.ytm = bond_price.ytm / 100
                            item.ytc = bond_price.ytc / 100
                            item.yield_error = bond_price.yield_error
                            bond_price_calc_manage.add_or_update(
                                price_key=f"{data[current_index][0]},{data[current_index][1]},{data[current_index][3]}",
                                key_type=3,
                                bond_price=bond_price)
                            bond_price_list.append(bond_price)
                            current_index = current_index + 1
        return error_info, bond_price_list
		
    @staticmethod
    def get_historical_position(security_account_list: List[Tuple], days: int,start_date:int =0,end_date:int=0) -> Tuple[ErrorInfo, DataFrame]:
        """
        查询历史持仓
        @param security_account_list: 券和账户的元组构成的列表，如[("600570.XSHG",account_info)]
        @param days:交易日天数
        @return:错误信息，持仓数据DataFrame
        """

        error_info: ErrorInfo = ErrorInfo()
        fields: List[str] = ["security", "investunit_id", "instance_id", "invest_type", "day_count","start_date","end_date"]
        data: List[list] = []
        for stock_and_account in security_account_list:
            if len(stock_and_account) == 2 and isinstance(stock_and_account[0], str) and isinstance(
                    stock_and_account[1], AccountInfo):
                security = stock_and_account[0]
                account: AccountInfo = stock_and_account[1]
                data.append([security, account.investunit_id, account.portfolio_id, account.invest_type.value, days,start_date,end_date])
            else:
                error_info.set_error_value(error_msg="入参格式错误")
                return error_info, None

        result_dict = make_request(function_id=FunctionID.GetHisPosition, fields=fields, data=data)
        converters = {
            "security": str,  # 代码
            "invest_type": int,  # 投资类型
            "position_type": int,  # 多空类型
            "initial_position": float,  # 期初数量
            "position": float,  # 当前持仓数量
            "available_position": float,  # 可用数量
            "yesterday_available_position": float,  # 昨仓可用数量
            "today_available_position": float,  # 今仓可用
            "buy_volume": float,  # 当日买成交数量
            "buy_value": float,  # 当日买成交金额
            "sell_volume": float,  # 当日卖成交数量
            "sell_value": float,  # 当日卖成交金额
            "unfilled_order_buy_quantity": float,  # 买挂单数量
            "unfilled_order_sell_quantity": float,  # 卖挂单数量
            "frozen_quantity": float,  # 冻结数量
            "cost": float,  # 持仓成本
            "total_fee": float,  # 持仓费用
            "investunit_id": int,  # 账户 ID
            "portfolio_id": int,  # 投资组合 ID
            "trade_date":int
        }
        error_info, data_dataframe = covert_csv_to_dataframe_tuple(msg=result_dict, converters=converters)
        if data_dataframe is None:
            return  error_info,data_dataframe
        data_dataframe['position_type'] = data_dataframe['position_type'].apply(
            lambda x: covert_to_enum(x, PositionType))
        data_dataframe['invest_type'] = data_dataframe['invest_type'].apply(lambda x: covert_to_enum(x, InvestType))
        return error_info, data_dataframe

    @staticmethod
    def group_communicate_register(gourp_name:str)->ErrorInfo:
        """
        策略组的消息的推送注册，查看能不注册相关的信息
        @param gourp_name:
        @param scheme_id:
        @return:
        """

        error_info: ErrorInfo = ErrorInfo()
        fields: List[str] = ["gourp_name"]
        data: List[list] = [gourp_name]

        result_dict = make_request(function_id=FunctionID.GroupPermissionQRY, fields=fields, data=data)
        from dataclasses import dataclass
        @dataclass
        class _pGroup:
            group_id:int

        error_info, data_dataframe = covert_message_to_p_class_tuple (msg=result_dict,data_name="info",data_class=_pGroup)
        return error_info,data_dataframe.group_id  if data_dataframe is not None  else None