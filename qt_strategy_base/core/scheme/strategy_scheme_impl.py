# -*- coding: utf-8 -*-
from typing import List, Dict

from qt_strategy_base import CombOrderData
from qt_strategy_base.api.strategy_api_context import SchemeInfo, ContextInfo
from qt_strategy_base.core.common import python_logger
from qt_strategy_base.core.common.constant import ApiRetType
from qt_strategy_base.core.common.dict_covert_to_model import covert_message_to_p_class_list_tuple
from qt_strategy_base.core.common.notice_sever import NoticeServer
from qt_strategy_base.core.common.public_func import covert_order_data_to_dataframe
from qt_strategy_base.core.model.model import PSecurityDetail, PSecurityBaseInfo, PStockDetailInfo, PBalanceAndAmount
from qt_strategy_base.core.scheme.callback_message_handle import CallbackMessageHandler
from qt_strategy_base.core.scheme.indicator import Indicator
from qt_strategy_base.core.scheme.strategy_cb_entrust_list_impl import CAlgoCBEntrustListImpl
from qt_strategy_base.core.scheme.strategy_scheme_stock_impl import SecurityDetailImpl, SecurityDetail
from qt_strategy_base.model.enum import SecurityDetailStatus, SchemeType, TradeType, ClearSpeed, SettleType, ClearType
from qt_strategy_base.model.error_info import ErrorInfo
from qt_strategy_base.core.scheme.strategy_order_impl import OrderData, get_mill, OrderDataImpl

class ContextImpl(ContextInfo):
    def __init__(self, scheme_id: int, spi_instance, message_handler: CallbackMessageHandler):
        from qt_strategy_base.core.scheme.strategy_entrust_list_impl import CAlgoEntrustListImpl
        from qt_strategy_base.core.scheme.strategy_scheme_stock_impl import SecurityDetailImpl
        self._scheme_id = scheme_id
        self._keep_final_state_entrust = False
        self._cancel_once = True
        self._recovery = False
        self._init = False
        self._single_account = False
        self._spi_instance = spi_instance
        self._message_handler = message_handler
        self._entrust_list = CAlgoEntrustListImpl(self)
        self._cb_entrust_list = CAlgoCBEntrustListImpl(self)
        self._scheme_stocks_list: List[SecurityDetailImpl] = []
        self._scheme_stocks_dict: Dict[str, SecurityDetailImpl] = {}
        self._code_scheme_stocks_dict: Dict[str, Dict[str, SecurityDetailImpl]] = {}

        self._scheme_status = SchemeType.UNINIT
        self._scheme_params = {}
        self._raw_data = {}
        self._callback_function_set = set()
        self._indicator = Indicator(self)
        from qt_strategy_base.core.scheme.group_communicate_impl import GroupManager

        self._group_mange=GroupManager(self)

    @property
    def scheme(self) -> SchemeInfo:
        return self

    @property
    def entrust_list(self):
        return self._entrust_list

    @property
    def cb_entrust_list(self):
        return self._cb_entrust_list

    def get_scheme_id(self):
        return self._scheme_id

    def get_param_info(self) -> dict:
        return self._scheme_params.copy()

    def get_scheme_status(self) -> SchemeType:
        return self._scheme_status

    def is_recovery(self) -> bool:
        return self._recovery

    def get_async_message_handler(self) -> CallbackMessageHandler:
        return self._message_handler

    @property
    def indicator(self) -> Indicator:
        return self._indicator

    @property
    def scheme_id(self) -> int:
        return self._scheme_id

    @property
    def init(self) -> bool:
        return self._init

    @init.setter
    def init(self, value):
        self._init = value

    @property
    def spi_instance(self):
        return self._spi_instance

    def is_inited(self) -> bool:
        return self._init

    @property
    def keep_final_state_entrust(self) -> bool:
        return self._keep_final_state_entrust

    @keep_final_state_entrust.setter
    def keep_final_state_entrust(self, value):
        self._keep_final_state_entrust = value

    @property
    def cancel_once(self) -> bool:
        return self._cancel_once

    @cancel_once.setter
    def cancel_once(self, value):
        self._cancel_once = value

    def on_scheme_init(self, msg_dict: dict) -> ErrorInfo:
        error_info = ErrorInfo()
        python_logger.info(f"方案[ID:{self.scheme_id} ]初始化开始")
        if msg_dict is None or len(msg_dict) == 0:
            error_info.error_no = ApiRetType.APIRETERR.value
            error_info.error_msg = "方案信息为空"
            return error_info
        error_info = self.gather_scheme_info(msg_dict)
        if error_info.error_no != ApiRetType.APIRETOK.value:
            return error_info

        error_info = self.gather_scheme_stocks_info(msg_dict)
        if error_info.error_no != ApiRetType.APIRETOK.value:
            return error_info

        self.set_scheme_status(status=SchemeType.RUNNING)
        self._init_callback_set()
        return error_info

    def _init_callback_set(self):
        for method_name in dir(self._spi_instance):
            if method_name.startswith('on_'):
                self._callback_function_set.add(method_name)

    def exit_function(self, method_name) -> bool:
        if method_name in self._callback_function_set:
            return True
        else:
            return False

    def gather_scheme_info(self, msg_dict: dict) -> ErrorInfo:
        error_info = ErrorInfo()
        # 保存原始的方案原始信息
        self._raw_data = msg_dict
        scheme_base_info = dict(
            zip(msg_dict['msg_content']['body']['scheme_base_info']['fields'],
                msg_dict['msg_content']['body']['scheme_base_info']['data']))
        scheme_code: str = scheme_base_info['scheme_code']
        recovery: int = scheme_base_info['recovery']
        self._recovery = False if recovery == 0 else True
        python_logger.info(f"=> 方案代码[{scheme_code}]")
        self._scheme_params = dict(
            zip(msg_dict['msg_content']['body']['scheme_params']['fields'],
                msg_dict['msg_content']['body']['scheme_params']['data']))
        if len(self._scheme_params) == 0:
            error_info.set_value(error_no=ApiRetType.APIRETERR.value, error_msg="没有策略参数")
            return error_info
        return error_info

    def gather_scheme_stocks_info(self, msg_dict) -> ErrorInfo:
        from qt_strategy_base.core.scheme.strategy_scheme_stock_impl import SecurityDetailImpl
        error_info = ErrorInfo()
        scheme_base_info = dict(
            zip(msg_dict['msg_content']['body']['scheme_base_info']['fields'],
                msg_dict['msg_content']['body']['scheme_base_info']['data']))
        topic_name: str = scheme_base_info['topic_name']
        python_logger.info(f"方案[ID:{self.scheme_id}]，主题名称:{topic_name}")

        error_info, scheme_stocks = covert_message_to_p_class_list_tuple(msg=msg_dict['msg_content'],
                                                                         data_name="scheme_stocks",
                                                                         data_class=PSecurityDetail)

        if scheme_stocks is None or len(scheme_stocks) == 0:
            error_info.set_error_value(error_msg="没有方案明细信息")
            return error_info
        error_info, stock_info_list = covert_message_to_p_class_list_tuple(msg=msg_dict['msg_content'],
                                                                           data_name="stock_infos",
                                                                           data_class=PSecurityBaseInfo)

        stock_info_dict: dict = {}
        for item in stock_info_list:
            stock_info_dict[item.scheme_ins_serial_no] = item

        for scheme_stock in scheme_stocks:

            stock_info = stock_info_dict.get(scheme_stock.id, None)
            if stock_info is None:
                python_logger.error(f"方案[{self.scheme_id}],明细[{scheme_stock.id}]的基础信息匹配失败")
                break
            scheme_stocks_impl = SecurityDetailImpl.gather_scheme_stocks_info(scheme_stock_info=scheme_stock,
                                                                              stock_info=stock_info,
                                                                              scheme=self,
                                                                              topic_name=topic_name)

            self._scheme_stocks_list.append(scheme_stocks_impl)
            self._scheme_stocks_dict[scheme_stocks_impl.id] = scheme_stocks_impl

            full_code: str = scheme_stocks_impl.get_stock_info().security

            scheme_stocks_dict = self._code_scheme_stocks_dict.get(full_code, {})
            scheme_stocks_dict[scheme_stocks_impl.id] = scheme_stocks_impl
            self._code_scheme_stocks_dict[full_code] = scheme_stocks_dict

        error_info, stock_detail_list = covert_message_to_p_class_list_tuple(msg=msg_dict['msg_content'],
                                                                             data_name="stock_details",
                                                                             data_class=PStockDetailInfo)

        stock_detail_dict = {}
        for stock_detail in stock_detail_list:
            balance_and_amount = stock_detail_dict.get(stock_detail.scheme_ins_serial_no, None)
            if balance_and_amount is None:
                stock_detail_dict[stock_detail.scheme_ins_serial_no] = [
                    PBalanceAndAmount(entrust_direction_out=stock_detail.real_deal_dir,
                                      entrust_amount=stock_detail.entrust_amount,
                                      entrust_balance=stock_detail.entrust_balance,
                                      deal_amount=stock_detail.deal_amount,
                                      deal_balance=stock_detail.deal_balance)
                ]
            else:
                balance_and_amount.append(PBalanceAndAmount(entrust_direction_out=stock_detail.real_deal_dir,
                                                            entrust_amount=stock_detail.entrust_amount,
                                                            entrust_balance=stock_detail.entrust_balance,
                                                            deal_amount=stock_detail.deal_amount,
                                                            deal_balance=stock_detail.deal_balance))

        for stock_detail_no in stock_detail_dict:
            scheme_stock = self._scheme_stocks_dict.get(stock_detail_no, None)
            if scheme_stock is not None:
                scheme_stock.recover_balance_and_amount(stock_detail_dict[stock_detail_no])
        return error_info

    def set_scheme_status(self, status: SchemeType) -> bool:
        b_change_flag = False
        if status == SchemeType.RUNNING:
            b_change_flag = self._scheme_status == SchemeType.UNINIT or self._scheme_status == SchemeType.PAUSED
        elif status == SchemeType.PAUSED:
            b_change_flag = self._scheme_status == SchemeType.RUNNING
        elif status == SchemeType.FINISHED or status == SchemeType.EXPIRED or status == SchemeType.CANCELLING:
            b_change_flag = self._scheme_status == SchemeType.UNINIT or self._scheme_status == SchemeType.PAUSED or self._scheme_status == SchemeType.RUNNING
        elif status == SchemeType.CANCELLED:
            b_change_flag = self._scheme_status == SchemeType.CANCELLING
        else:
            pass
        if b_change_flag and self._scheme_status.value != status.value:
            self._scheme_status = status
        return b_change_flag

    def set_scheme_stocks_status(self, e_stock_status: SecurityDetailStatus):
        for scheme_stock in self._scheme_stocks_list:
            scheme_stock.set_scheme_stock_status(e_stock_status)

    def get_scheme_stocks_count(self) -> int:
        return len(self._scheme_stocks_list)

    def get_scheme_stock_by_index(self, index: int):
        scheme_stock = None
        if 0 <= index < len(self._scheme_stocks_list):
            scheme_stock = self._scheme_stocks_list[index]
        return scheme_stock

    def get_scheme_stock_by_ins_code(self, scheme_ins_code: str):
        scheme_stock = self._scheme_stocks_dict.get(scheme_ins_code, None)
        return scheme_stock

    def send_entrust_req(self, entrust_info: OrderDataImpl, clear_speed: ClearSpeed, entrust_type: str,
                         is_nicked: bool, counterparty_order_id: str, trade_type: TradeType):
        NoticeServer.send_entrust_req(scheme_id=self._scheme_id, entrust_info=entrust_info, clear_speed=clear_speed,
                                      entrust_type=entrust_type, is_nicked=is_nicked,
                                      counterparty_order_id=counterparty_order_id, trade_type=trade_type)

    def do_cancel_entrust_req(self, entrust_info: OrderData, cancel_once: int):
        NoticeServer.cancel_entrust_req(scheme_id=self._scheme_id, entrust_info=entrust_info, cancel_once=cancel_once)

    def cancel_order_by_internal_id(self, order_id) -> ErrorInfo:
        error_info = ErrorInfo()
        entrust_info: OrderData = self._entrust_list.find_entrust(order_id=order_id)
        if entrust_info is not None:
            if self.cancel_once:
                if get_mill() - entrust_info.get_last_cancel_time() < 500:
                    python_logger.debug(f"子单[{order_id}]撤单频率过快。请稍候再试")
                    error_info.set_value(error_no=ApiRetType.APIRETERR.value,
                                         error_msg=f"子单[{order_id}]撤单频率过快。请稍候再试")
                    return error_info
            if entrust_info.get_cancel_type() != 1:  # 正在撤单的不再发起撤单
                cancel_once: int = 0
                if self.cancel_once:
                    cancel_once = 1
                self.do_cancel_entrust_req(entrust_info=entrust_info, cancel_once=cancel_once)
                entrust_info.set_cancel_type(1)
                entrust_info.update_last_cancel_time()
            return error_info
        else:
            error_info.set_value(error_no=ApiRetType.APIRETERR.value, error_msg=f"没有找到[{order_id}]对应的委托")
            return error_info


    def recover_entrust(self, entrust_info: OrderData):
        self._entrust_list.recover_entrust(entrust_info=entrust_info)

    def _print_strategy_param_modify(self, msg_dict: dict) -> str:
        msg = ""
        for param_name, old_value in self._scheme_params.items():
            new_vale = msg_dict.get(param_name, "")
            if old_value != new_vale:
                msg = f'{msg}[{param_name}:{old_value}->{new_vale}]'
        python_logger.info(msg)
        print(msg)
        return msg

    def do_strategy_modify(self, param_dict: dict) -> ErrorInfo:
        error_info: ErrorInfo = ErrorInfo.ok()
        self._print_strategy_param_modify(msg_dict=param_dict)
        self._scheme_params = param_dict
        return error_info

    def get_internal_orders(self, internal_ids: list[str] = None):
        internal_order_list: list[OrderData] = []
        if internal_ids is None:
            internal_order_list = self._entrust_list.get_iterator()
        else:
            for internal_id in internal_ids:
                internal_order = self._entrust_list.find_entrust(order_id=internal_id)
                if internal_order is not None:
                    internal_order_list.append(internal_order)
        return covert_order_data_to_dataframe(order_list=internal_order_list)

    def get_parameters(self) -> dict:
        return self._scheme_params.copy()

    def get_security_list(self) -> list[str]:
        security_list = set()
        for detail in self._scheme_stocks_list:
            security_list.add(detail.security)
        return list(security_list)

    def get_status(self) -> SchemeType:
        return self._scheme_status

    def get_security_details(self) -> list[SecurityDetail]:
        return self._scheme_stocks_list

    def get_security_detail_by_id(self, id) -> SecurityDetail:
        return self._scheme_stocks_dict.get(id, None)

    def get_security_details_by_security(self, security) -> list[SecurityDetail]:
        scheme_stock_info_dict: Dict[str, SecurityDetailImpl] = self._code_scheme_stocks_dict.get(security, None)
        if scheme_stock_info_dict is not None and len(scheme_stock_info_dict) != 0:
            return list(scheme_stock_info_dict.values())
        else:
            return []

    def add(self, key: str, value: [str, float, int, bool], unit: str = "", order: int = 0):
        scheme_ins_code: str = ""
        index = f"{self._scheme_id}-{scheme_ins_code}-{key}"
        self._key_value_dict[index] = (key, str(value), unit, order, str(scheme_ins_code))

    def send_cb_entrust_req(self, entrust_info: CombOrderData, replace_order_id: int, is_nicked: bool,
                            clear_speed: ClearSpeed, entrust_type: int, expire_time: int, iceberg_quantity: float,
                            settle_type: SettleType, clear_type: ClearType):
        NoticeServer.send_cb_entrust_req(scheme_id=self._scheme_id, entrust_info=entrust_info,
                                         replace_order_id=replace_order_id, is_nicked=is_nicked,
                                         clear_speed=clear_speed, entrust_type=entrust_type,
                                         expire_time=expire_time, iceberg_quantity=iceberg_quantity,
                                         settle_type=settle_type, clear_type=clear_type)
