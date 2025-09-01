# -*- coding: utf-8 -*-
from typing import List, Any

from qt_strategy_base import OrderData
from qt_strategy_base.core.cache.global_params import GlobalParams
from qt_strategy_base.core.common.constant import FunctionID
from qt_strategy_base.core.common.request import make_request_no_recv, make_response_no_recv
from qt_strategy_base.core.model.enum import LogSource, EMessageType
from qt_strategy_base.core.model.model import PCombOrderData
from qt_strategy_base.core.scheme.strategy_order_impl import OrderDataImpl
from qt_strategy_base.model.comb_order import CombOrderData
from qt_strategy_base.model.enum import MessageType, ClearSpeed, TradeType, ClearType, SettleType


class NoticeServer:

    @staticmethod
    def scheme_finished(scheme_id: int, message: str = ""):
        fields: List[str] = ["message"]
        data: List[list] = [[message]]
        make_request_no_recv(scheme_id=scheme_id, function_id=FunctionID.CallSchemeFinished, fields=fields, data=data)

    @staticmethod
    def scheme_pause(scheme_id: int, is_cancel_order: bool, message: str = ""):
        is_cancel_order_value = 1 if is_cancel_order else 0
        fields: List[str] = ["message", "is_cancel_order"]
        data: List[list] = [[message, is_cancel_order_value]]
        make_request_no_recv(scheme_id=scheme_id, function_id=FunctionID.CallSchemePause, fields=fields, data=data)

    @staticmethod
    def scheme_resume(scheme_id: int, message: str = ""):
        fields: List[str] = ["message"]
        data: List[list] = [[message]]
        make_request_no_recv(scheme_id=scheme_id, function_id=FunctionID.CallSchemeRun, fields=fields, data=data)

    @staticmethod
    def scheme_init_result(package_id: int, scheme_id: int, error_no: int, error_msg: str):
        fields: List[str] = ["scheme_id", "error_no", "error_msg"]
        data: List[list] = [[scheme_id, error_no, error_msg]]
        make_response_no_recv(scheme_id=scheme_id, package_id=package_id, function_id=FunctionID.CreateScheme,
                              fields=fields, data=data)

    @staticmethod
    def strategy_param_modify_result(package_id: int, scheme_id: int, error_no: int, error_msg: str):
        fields: List[str] = ["scheme_id", "error_no", "error_msg"]
        data: List[list] = [[scheme_id, error_no, error_msg]]
        make_response_no_recv(scheme_id=scheme_id, package_id=package_id, function_id=FunctionID.StrategyParamModify,
                              fields=fields, data=data)

    @staticmethod
    def send_log(message: str, message_type: int, log_source: int = LogSource.FRAMEWORK.value):
        fields: List[str] = ["msg", "msg_type", "log_source", "strategy_id"]
        data: List[list] = [[message, message_type, log_source, GlobalParams().strategy_id]]
        if GlobalParams().log_level == "1" and message_type > EMessageType.INFO.value:
            return
        if GlobalParams().log_level == "2" and message_type > EMessageType.WARNING.value:
            return
        if GlobalParams().log_level == "3" and message_type != EMessageType.ERROR.value:
            return
        make_request_no_recv(scheme_id=0, function_id=FunctionID.SendLogMessage, fields=fields, data=data)

    @staticmethod
    def push_key_value_count(scheme_id: int, key_value_info):
        fields: List[str] = ["param_name", "param_value", "param_unit", "order_id", "scheme_ins_serial_no"]
        data: list = key_value_info
        make_request_no_recv(scheme_id=scheme_id, function_id=FunctionID.PushKeyValueCount, fields=fields, data=data)

    @staticmethod
    def send_message(content: str, message_type=MessageType.INFO):
        fields: List[str] = ["message", "msg_type"]
        data: List[Any] = [[content, message_type.value]]
        make_request_no_recv(scheme_id=0, function_id=FunctionID.SystemMessage, fields=fields, data=data)

    @staticmethod
    def thread_exception_handle(scheme_id: int, package_id: str, exception_cause: str, thread_id: int):
        fields: List[str] = ["package_id", "exception_cause", "thread_id"]
        data: List[Any] = [[package_id, exception_cause, thread_id]]
        make_request_no_recv(scheme_id=scheme_id, function_id=FunctionID.CallBackThreadException, fields=fields,
                             data=data)

    @staticmethod
    def send_entrust_req(scheme_id: int, entrust_info: OrderDataImpl, clear_speed: ClearSpeed, entrust_type: int,
                         is_nicked: bool, counterparty_order_id: str, trade_type: TradeType):
        if entrust_info.is_limit():
            ins_price_type = "1"
        else:
            ins_price_type = "2"

        fields: List[str] = ["scheme_id", "scheme_ins_serial_no", "algo_ordid", "entrust_direction",
                             "futures_direction", "close_direction", "entrust_price", "entrust_amount",
                             "ins_price_type", "remark", "clear_speed", "entrust_type", "is_nicked",
                             "counterparty_order_id", "bond_trade_type"]
        side = 0 if entrust_info.side is None else entrust_info.side.value
        direction = 0 if entrust_info.direction is None else entrust_info.direction.value
        close_type = 0 if entrust_info.close_type is None else entrust_info.close_type.value
        clear_speed_value = -1 if clear_speed is None else clear_speed.value
        is_nicked_value = 1 if is_nicked else 0
        trade_type_value = 0 if trade_type is None else trade_type.value
        data: List[list] = [
            [scheme_id, entrust_info.security_detail_id, entrust_info.internal_id,
             side, direction, close_type, entrust_info.price, entrust_info.quantity,
             ins_price_type, entrust_info.remark, clear_speed_value, entrust_type, is_nicked_value,
             counterparty_order_id, trade_type_value]]
        make_request_no_recv(scheme_id=scheme_id, function_id=FunctionID.SendEntrustReq, fields=fields,
                             data=data)

    @staticmethod
    def cancel_entrust_req(scheme_id: int, entrust_info, cancel_once: int):
        fields: List[str] = ["scheme_id", "scheme_ins_serial_no", "algo_ordid", "cancel_flag"]
        data: List[list] = [
            [scheme_id, entrust_info.security_detail_id, entrust_info.internal_id, cancel_once]]
        make_request_no_recv(scheme_id=scheme_id, function_id=FunctionID.CancelEntrustBySubID, fields=fields,
                             data=data)

    @staticmethod
    def send_cb_entrust_req(scheme_id: int, entrust_info: CombOrderData, replace_order_id: int, is_nicked: bool,
                            clear_speed: ClearSpeed, entrust_type: int, expire_time: int, iceberg_quantity: float,
                            settle_type: SettleType, clear_type: ClearType):
        fields: List[str] = ["scheme_id", "scheme_ins_serial_no", "algo_ordid", "security", "buy_direction",
                             "buy_price", "buy_quantity", "buy_close_type", "sell_direction", "sell_price",
                             "sell_quantity", "sell_close_type", "replace_order_id", "is_nicked", "clear_speed",
                             "entrust_type", "expire_time", "iceberg_quantity", "settle_type", "clear_type"]
        buy_direction = 0 if entrust_info.buy_direction is None else entrust_info.buy_direction.value
        buy_close_type = 0 if entrust_info.buy_close_type is None else entrust_info.buy_close_type.value
        sell_direction = 0 if entrust_info.sell_direction is None else entrust_info.sell_direction.value
        sell_close_type = 0 if entrust_info.sell_close_type is None else entrust_info.sell_close_type.value
        is_nicked_value = 1 if is_nicked else 0
        clear_speed_value = -1 if clear_speed is None else clear_speed.value
        settle_type_value = 0 if settle_type is None else settle_type.value
        clear_type_value = 0 if clear_type is None else clear_type.value
        data: List[list] = [[scheme_id, entrust_info.security_detail_id, entrust_info.internal_id,
                             entrust_info.security, buy_direction, entrust_info.buy_price,
                             entrust_info.buy_quantity, buy_close_type, sell_direction, entrust_info.sell_price,
                             entrust_info.sell_quantity, sell_close_type, replace_order_id, is_nicked_value,
                             clear_speed_value, entrust_type, expire_time, iceberg_quantity, settle_type_value,
                             clear_type_value]]
        make_request_no_recv(scheme_id=scheme_id, function_id=FunctionID.SendCBEntrustReq, fields=fields,
                             data=data)

    @staticmethod
    def cancel_comb_order(scheme_id: int, internal_id: str, order_id: int):
        fields: List[str] = ["scheme_id", "internal_id", "order_id"]
        data: List[list] = [[scheme_id, internal_id, order_id]]
        make_request_no_recv(scheme_id=scheme_id, function_id=FunctionID.CancelCBEntrustReq, fields=fields, data=data)


    @staticmethod
    def cancel_group_suber(scheme_id: int,group_name:str):
        fields: List[str] = ["group_name"]
        data: List[list] = [[group_name]]
        make_request_no_recv(scheme_id=scheme_id, function_id=FunctionID.UnsubroupCommuntion, fields=fields, data=data)

    @staticmethod
    def group_msg_push(key:str,data,data_length:int,type_name:str,scheme_id:int,group_name:str,group_id:int):
        fields: List[str] = ["key", "data", "length","type_name","group_name","group_id"]
        temp=data
        if type_name=="I":
            if not isinstance(data,int):
                return
        elif type_name=="D":
            if isinstance(data,int):
                temp= int(data)
            elif not isinstance( data,float):
                return
        elif type_name=="S":
            if not  isinstance(data,str):
                return
        elif type(data) is bytes:
            import  base64
            encoded = base64.b64encode(data)
            temp=encoded.decode('utf-8')
            print(temp)
        else:
            return
        data: List[list] = [[key,temp,data_length,type_name,group_name,group_id]]
        make_request_no_recv(scheme_id=scheme_id, function_id=FunctionID.GroupMsgPush, fields=fields, data=data)