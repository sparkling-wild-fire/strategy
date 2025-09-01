# -*- coding: utf-8 -*-
from typing import Any, Dict, List

from qt_strategy_base.common import fleq
from qt_strategy_base.core.cache.bond_hq_cache_manage import BondHQCacheManageBase
from qt_strategy_base.core.cache.intrabak_bond_hq_manage import IntrabakBondHqManage
from qt_strategy_base.core.cache.sub_scheme_manage import SubSchemeManager
from qt_strategy_base.core.cache.xbond_hq_cache_manage import XBondHQCacheManageBase
from qt_strategy_base.core.common import python_logger
from qt_strategy_base.core.cache.factor_cache_manage import FactorCacheManageBase
from qt_strategy_base.core.cache.hq_cache_manage import HQCacheManage
from qt_strategy_base.core.cache.scheme_manage import SchemeManage
from qt_strategy_base.core.common.constant import FunctionType, FunctionID
from qt_strategy_base.core.common.dict_covert_to_model import covert_message_to_dict_tuple, \
    covert_message_to_class_tuple, covert_message_to_order_class_tuple, covert_message_to_order_class_list_tuple, \
    covert_message_to_p_class_tuple, covert_message_to_class_list_tuple, \
    covert_message_to_p_class_list_tuple
from qt_strategy_base.core.common.notice_sever import NoticeServer
from qt_strategy_base.core.common.public_func import fix_date_time_to_dt, covert_to_enum
from qt_strategy_base.core.model.model import PSnapshotData, POrderData, \
    PPositionData, PTradeData, PMarketDutyData, PFactor, PAlgoScheme, PAlgoDetail, PQDBJHqInfo, PCJHqInfo, \
    PCombOrderData, PXBondBaseInfo, PXBondOrder, PYHJBondMMInfo, PYHJBondMMOrder,PGroupMsgData
from qt_strategy_base.core.scheme.strategy_cb_order_impl import CombOrderDataImpl
from qt_strategy_base.core.scheme.strategy_scheme_impl import ContextImpl
from qt_strategy_base.core.scheme.strategy_scheme_stock_impl import SecurityDetailImpl
from qt_strategy_base.model.comb_order import CombOrderData

from qt_strategy_base.model.enum import SchemeType, SecurityDetailStatus, PushType, OrderStatus
from qt_strategy_base.model.error_info import ErrorInfo
from qt_strategy_base.core.scheme.strategy_order_impl import OrderData, OrderDataImpl
from qt_strategy_base.model.strategy_api_data import SnapshotData, PositionData, TradeData, MarketDutyData, Factor, \
    BondClickHq, BondQDBJInfo, XBondOrder, XBondInfo, YHJBondMMOrder, YHJBondMMInfo


class FunctionInfo:
    def __init__(self, function_id: int, function_type: int, function: Any):
        self._function_id: int = function_id
        self._function_type: int = function_type
        self._function: Any = function

    @property
    def function_type(self) -> int:
        return self._function_type

    @property
    def function(self) -> Any:
        return self._function


def initialize(context: ContextImpl, msg: dict):
    try:
        error_info: ErrorInfo = context.on_scheme_init(msg)
        if error_info.has_error():
            python_logger.error(f"方案[ID:{context.scheme_id}]初始化失败[{error_info.error_msg}]")
            NoticeServer.scheme_init_result(package_id=msg['package_id'], scheme_id=context.scheme_id, error_no=1,
                                            error_msg=error_info.error_msg)
            return
        error_info = context.spi_instance.initialize(context)
        if error_info is None:
            error_info = ErrorInfo.ok()
        if error_info.has_error():
            python_logger.error(f"方案[ID:{context.scheme_id}]初始化失败[{context.scheme_id}]")
            NoticeServer.scheme_init_result(package_id=msg['package_id'], scheme_id=context.scheme_id, error_no=1,
                                            error_msg=error_info.error_msg)
        else:
            context.init = True
            python_logger.info(f"方案[ID:{context.scheme_id}初始化完成]")
            NoticeServer.scheme_init_result(package_id=msg['package_id'], scheme_id=context.scheme_id, error_no=0,
                                            error_msg="")
    except Exception as e:
        NoticeServer.scheme_init_result(package_id=msg['package_id'], scheme_id=context.scheme_id, error_no=1,
                                        error_msg=str(e))
        raise e


def on_pause(context: ContextImpl, msg: dict):
    if context.is_inited():
        python_logger.info(f"方案[ID{context.scheme_id}收到暂停请求")
        context.set_scheme_status(SchemeType.PAUSED)
        context.set_scheme_stocks_status(SecurityDetailStatus.PAUSED)
        if context.exit_function(method_name="on_pause"):
            context.spi_instance.on_pause(context)
    else:
        python_logger.warning(f"方案[ID:{context.scheme_id}]此时尚未初始化，无法处理方案暂停请求")


def on_resume(context: ContextImpl, msg: dict):
    if context.is_inited():
        python_logger.info(f"方案[[ID:{context.scheme_id}收到恢复请求")
        context.set_scheme_status(SchemeType.RUNNING)
        context.set_scheme_stocks_status(SecurityDetailStatus.RUNNING)
        if context.exit_function(method_name="on_resume"):
            context.spi_instance.on_resume(context)
    else:
        python_logger.warning(f"方案[ID:{context.scheme_id}]此时尚未初始化，无法处理方案恢复")


def on_modify(context: ContextImpl, msg: dict):
    param_error_info, param_dict = covert_message_to_dict_tuple(msg=msg['msg_content'], data_name="scheme_params")
    scheme_start_time = param_dict.get("scheme_start_time", None)
    scheme_end_time = param_dict.get("scheme_end_time", None)
    if scheme_start_time:
        param_dict["scheme_start_time"] = scheme_start_time
    if scheme_end_time:
        param_dict["scheme_end_time"] = scheme_end_time

    if context.exit_function(method_name="on_modify"):
        result_error_info: ErrorInfo = context.spi_instance.on_modify(context, param_dict)
    else:
        result_error_info: ErrorInfo = ErrorInfo.ok()
    if result_error_info is None:
        result_error_info = ErrorInfo.ok()
    if not result_error_info.has_error():
        result_error_info = context.do_strategy_modify(param_dict=param_dict)

    NoticeServer.strategy_param_modify_result(package_id=msg['package_id'], scheme_id=context.scheme_id,
                                              error_no=result_error_info.error_no,
                                              error_msg=result_error_info.error_msg)


def on_cancel(context: ContextImpl, msg: dict):
    if context.is_inited():
        python_logger.info(f"方案[ID:{context.scheme_id}]收到撤销请求")
        context.set_scheme_status(SchemeType.CANCELLING)
        context.set_scheme_stocks_status(SecurityDetailStatus.CANCELLING)
        if context.exit_function(method_name="on_cancel"):
            context.spi_instance.on_cancel(context)
    else:
        python_logger.warning(f"方案[ID:{context.scheme_id}]此时尚未初始化，无法处理方案撤销请求")


def on_entrust_req_accept(context: ContextImpl, msg: dict):
    if context.is_inited():
        if msg is None or len(msg) == 0:
            return

        error_info, result_data = covert_message_to_order_class_tuple(msg=msg['msg_content'], data_name="info",
                                                                      data_class=POrderData,
                                                                      return_class=OrderDataImpl)
        if error_info.has_error():
            python_logger.error(f"on_entrust_req_accept收到异常数据,错误原因：{error_info.error_msg}")
            return
        if result_data is None:
            python_logger.error(f"on_entrust_req_accept收到异常数据")
            return

        internal_id = result_data.internal_id
        scheme_ins_code: str = result_data.security_detail_id
        price: float = result_data.price
        quantity: float = result_data.quantity

        entrust_info: OrderData = context.entrust_list.update_un_final_state_entrust(new_order_data=result_data)
        if error_info is None:
            python_logger.error(f"处理子单委托确认时找不到对应的子单委托[ID:{internal_id}]")
            return
        python_logger.info(
            f"方案[ID:{context.scheme_id}]-方案明细[ID:{scheme_ins_code}]-子单[ID:{internal_id}]委托确认, 委托价格[{price}], 原委托数量[{quantity}]")
        if context.exit_function(method_name="on_order"):
            context.spi_instance.on_order(context, entrust_info, PushType.ORDER_RECEIVE)
    else:
        python_logger.error(f"方案[ID: {context.scheme_id}]此时尚未初始化，无法处理子单委托确认消息")


def on_entrust_req_reject_by_c(context: ContextImpl, msg: dict):
    if context.is_inited():
        if msg is None or len(msg) == 0:
            python_logger.error(f"on_entrust_req_reject_by_c收到异常数据")
            return
        error_info, result_dict = covert_message_to_dict_tuple(msg=msg['msg_content'], data_name="info")
        internal_id: str = result_dict.get("algo_ordid", "")
        revoke_cause: str = result_dict.get("revoke_cause", "")
        entrust_type: float = result_dict.get("entrust_type", 0)

        if error_info.has_error():
            python_logger.error(f"on_entrust_req_reject_by_c收到异常数据,错误原因：{error_info.error_msg}")
            return

        if entrust_type == 1:
            entrust = context.entrust_list.find_entrust(order_id=internal_id)
            if entrust is not None:
                entrust.set_revoke_cause(revoke_cause)
                entrust.set_status(OrderStatus.WASTE)
                scheme_ins_code: str = entrust.security_detail_id
                entrust_price: float = entrust.price
                entrust_amount: float = entrust.quantity
                python_logger.info(
                    f"方案[ID:{context.scheme_id}]-方案明细[ID:{scheme_ins_code}]-子单[ID:{internal_id}]拒绝, 委托价格[{entrust_price}],委托数量[{entrust_amount}],委托拒绝原因：[{revoke_cause}]")
                entrust_info: OrderData = context.entrust_list.update_final_state_entrust(new_order_data=entrust)
                if entrust_info is None:
                    python_logger.error(f"处理子单委托拒绝时找不到对应的子单委托[ID:{internal_id}]")
                    return
                scheme_stock: SecurityDetailImpl = context.get_scheme_stock_by_ins_code(scheme_ins_code)
                if scheme_stock is None:
                    python_logger.error(f"处理子单委托拒绝时找不到对应的方案明细[ID:{scheme_ins_code}]")
                else:
                    scheme_stock.on_entrust_req_reject(entrust_info=entrust_info, entrust_amount=entrust_info.quantity,
                                                       entrust_price=entrust_price)
                if context.exit_function(method_name="on_order"):
                    context.spi_instance.on_order(context, entrust_info, PushType.ORDER_FAIL)
        elif entrust_type == 2:
            current_entrust = context.cb_entrust_list.find_entrust(internal_id=internal_id)
            if current_entrust is not None and current_entrust.status is not OrderStatus.WASTE:
                reject_entrust = context.cb_entrust_list.entrust_reject(internal_id=internal_id,
                                                                        revoke_cause=revoke_cause)
                if reject_entrust is not None and context.exit_function(method_name="on_comb_order"):
                    context.spi_instance.on_comb_order(context, reject_entrust, PushType.ORDER_FAIL)
    else:
        python_logger.error(f"方案[ID: {context.scheme_id}]此时尚未初始化，无法处理委托拒绝消息")


def on_entrust_req_reject(context: ContextImpl, msg: dict):
    if context.is_inited():
        if msg is None or len(msg) == 0:
            python_logger.error(f"on_entrust_req_reject收到异常数据")
            return

        error_info, result_data = covert_message_to_order_class_tuple(msg=msg['msg_content'], data_name="info",
                                                                      data_class=POrderData,
                                                                      return_class=OrderDataImpl)
        if error_info.has_error():
            python_logger.error(f"on_entrust_req_reject收到异常数据,错误原因：{error_info.error_msg}")
            return
        if result_data is None:
            python_logger.error(f"on_entrust_req_reject收到异常数据")
            return
        scheme_ins_code: str = result_data.security_detail_id
        internal_id: str = result_data.internal_id
        price: float = result_data.price
        quantity: float = result_data.quantity
        revoke_cause: str = result_data.revoke_cause
        python_logger.info(
            f"方案[ID:{context.scheme_id}]-方案明细[ID:{scheme_ins_code}]-子单[ID:{internal_id}]拒绝, 委托价格[{price}],委托数量[{quantity}],委托拒绝原因：[{revoke_cause}]")

        entrust_info: OrderData = context.entrust_list.update_final_state_entrust(new_order_data=result_data)
        if entrust_info is None:
            python_logger.error(f"处理子单委托拒绝时找不到对应的子单委托[ID:{internal_id}]")
            return
        scheme_stock: SecurityDetailImpl = context.get_scheme_stock_by_ins_code(scheme_ins_code)
        if scheme_stock is None:
            python_logger.error(f"处理子单委托拒绝时找不到对应的方案明细[ID:{scheme_ins_code}]")
        else:
            scheme_stock.on_entrust_req_reject(entrust_info=entrust_info, entrust_amount=entrust_info.quantity,
                                               entrust_price=price)
        if context.exit_function(method_name="on_order"):
            context.spi_instance.on_order(context, entrust_info, PushType.ORDER_FAIL)
    else:
        python_logger.error(f"方案[ID: {context.scheme_id}]此时尚未初始化，无法处理委托拒绝消息")


def on_entrust_confirm(context: ContextImpl, msg: dict):
    if context.is_inited():
        if msg is None or len(msg) == 0:
            python_logger.error(f"on_entrust_confirm收到异常数据")
            return
        error_info, result_data = covert_message_to_order_class_tuple(msg=msg['msg_content'], data_name="info",
                                                                      data_class=POrderData,
                                                                      return_class=OrderDataImpl)
        if error_info.has_error():
            python_logger.error(f"on_entrust_confirm收到异常数据,错误原因：{error_info.error_msg}")
            return
        if result_data is None:
            python_logger.error(f"on_entrust_confirm收到异常数据")
            return
        scheme_ins_code: str = result_data.security_detail_id
        internal_id: str = result_data.internal_id
        price: float = result_data.price
        entrust_amount: float = result_data.quantity
        python_logger.debug(
            f"方案[ID:{context.scheme_id}]-方案明细[ID:{scheme_ins_code}]-子单[ID:{internal_id}]委托确认, 委托数量[{entrust_amount}], 委托价格[{price}]")
        entrust_info = context.entrust_list.update_un_final_state_entrust(new_order_data=result_data)
        if entrust_info is None:
            python_logger.error(f"处理子单委托确认时找不到对应的子单委托[ID:{internal_id}]")
            return
        if context.exit_function(method_name="on_order"):
            context.spi_instance.on_order(context, entrust_info, PushType.ORDER_CONFIRM)

    else:
        python_logger.error(f"方案[ID: {context.scheme_id}]此时尚未初始化，无法处理委托拒绝消息")


def on_trade(context: ContextImpl, msg: dict):
    if context.is_inited():
        if msg is None or len(msg) == 0:
            python_logger.error(f"on_trade收到异常数据")
            return
        error_info, trade_result_data = covert_message_to_class_tuple(msg=msg['msg_content'], data_name="info",
                                                                      data_class=PTradeData,
                                                                      return_class=TradeData)

        if error_info.has_error():
            python_logger.error(f"on_trade收到异常成交数据,错误原因：{error_info.error_msg}")
            return
        if trade_result_data is None:
            python_logger.error(f"on_trade收到异常成交数据")
            return

        order_result_data = context.entrust_list.find_entrust(order_id=trade_result_data.internal_id)
        if order_result_data is None:
            python_logger.error(f"on_trade收到异常委托数据")
            return

        scheme_ins_code: str = trade_result_data.security_detail_id
        internal_id: str = trade_result_data.internal_id
        total_volume: float = trade_result_data.total_volume
        total_value: float = trade_result_data.total_value
        order_result_data.set_filled_quantity(total_volume)
        order_result_data.set_filled_value(total_value)
        python_logger.info(
            f"方案[ID:{context.scheme_id}]-方案明细[ID:{scheme_ins_code}]-子单[ID:{internal_id}]收到成交消息, 成交数量[{total_value}], 成交金额[{total_volume}]")

        if fleq(order_result_data.quantity, order_result_data.filled_quantity):
            entrust_info: OrderData = context.entrust_list.update_final_state_entrust(new_order_data=order_result_data)

        else:
            entrust_info: OrderData = context.entrust_list.update_un_final_state_entrust(
                new_order_data=order_result_data)

        if entrust_info is None:
            python_logger.error(f"处理子单委托成交时找不到对应的子单委托[ID:{internal_id}]")
            return

        context.get_scheme_stock_by_ins_code(scheme_ins_code=scheme_ins_code)
        scheme_stock: SecurityDetailImpl = context.get_scheme_stock_by_ins_code(scheme_ins_code=scheme_ins_code)
        if scheme_stock is None:
            python_logger.error(f"处理子单委托成交时找不到对应的方案明细[ID:{scheme_ins_code}]")
        else:
            scheme_stock.on_trade(entrust_info=entrust_info, total_volume=total_volume, total_value=total_value)

        if context.exit_function(method_name="on_trade"):
            context.spi_instance.on_trade(context, trade_result_data)

        if context.exit_function(method_name="on_order"):
            context.spi_instance.on_order(context, entrust_info, PushType.TRADE_RECEIVE)

    else:
        python_logger.error(f"方案[ID:{context.scheme_id}]此时尚未初始化，无法处理成交消息")


def on_entrust_waste(context: ContextImpl, msg: dict):
    if context.is_inited():
        if msg is None or len(msg) == 0:
            return
        error_info, result_data = covert_message_to_order_class_tuple(msg=msg['msg_content'], data_name="info",
                                                                      data_class=POrderData,
                                                                      return_class=OrderDataImpl)

        if error_info.has_error():
            python_logger.error(f"on_entrust_waste收到异常数据,错误原因：{error_info.error_msg}")
            return
        if result_data is None:
            python_logger.error(f"on_entrust_waste收到异常数据")
            return

        scheme_ins_code: str = result_data.security_detail_id
        internal_id: str = result_data.internal_id
        price: float = result_data.price
        quantity: float = result_data.quantity
        revoke_cause: str = result_data.revoke_cause
        python_logger.info(
            f"方案[ID:{context.scheme_id}]-方案明细[ID:{scheme_ins_code}]-子单[ID:{internal_id}]废单, 委托数量[{quantity}], 委托价格[{price}], 废单原因[{revoke_cause}]")

        entrust_info = context.entrust_list.update_final_state_entrust(new_order_data=result_data)
        if entrust_info is None:
            python_logger.error(f"处理子单委托废单时找不到对应的子单委托[ID:{internal_id}]")
            return
        scheme_stock = context.get_scheme_stock_by_ins_code(scheme_ins_code=scheme_ins_code)
        if scheme_stock is None:
            python_logger.error(f"处理子单委托废单时找不到对应的方案明细[ID:{scheme_ins_code}]")
        else:
            scheme_stock.on_entrust_waste(entrust_info=entrust_info, entrust_amount=quantity,
                                          entrust_price=price)
        if context.exit_function(method_name="on_order"):
            context.spi_instance.on_order(context, entrust_info, PushType.ORDER_FAIL)
    else:
        python_logger.error(f"方案[ID: {context.scheme_id}]此时尚未初始化，无法处理废单回调")


def on_entrust_cancelled(context: ContextImpl, msg: dict):
    if context.is_inited():
        if msg is None or len(msg) == 0:
            return
        error_info, result_data = covert_message_to_order_class_tuple(msg=msg['msg_content'], data_name="info",
                                                                      data_class=POrderData,
                                                                      return_class=OrderDataImpl)
        if error_info.has_error():
            python_logger.error(f"on_entrust_cancelled收到异常数据,错误原因：{error_info.error_msg}")
            return
        if result_data is None:
            python_logger.error(f"on_entrust_cancelled收到异常数据")
            return
        scheme_ins_code: str = result_data.security_detail_id
        internal_id: str = result_data.internal_id
        cancel_value: float = result_data.get_cancel_value()
        cancel_quantity: float = result_data.cancel_quantity
        python_logger.info(
            f"方案[ID:{context.scheme_id}]-方案明细[ID:{scheme_ins_code}]-子单[ID:{internal_id}]撤成, 撤成数量[{cancel_quantity}],撤成金额[{cancel_value}]")

        entrust_info = context.entrust_list.update_final_state_entrust(new_order_data=result_data)
        if entrust_info is None:
            python_logger.error(f"处理子单委托撤成时找不到对应的子单委托[ID:{internal_id}]")
            return

        scheme_stock = context.get_scheme_stock_by_ins_code(scheme_ins_code=scheme_ins_code)
        if scheme_stock is None:
            python_logger.error(f"处理子单委托撤成时找不到对应的方案明细[ID:{scheme_ins_code}]")
        else:
            scheme_stock.on_entrust_cancelled(entrust_info=entrust_info, cancelled_amount=cancel_quantity,
                                              cancelled_balance=cancel_value)
        if context.exit_function(method_name="on_order"):
            context.spi_instance.on_order(context, entrust_info, PushType.CANCEL_CONFIRM)

    else:
        python_logger.error(f"方案[ID:{context.scheme_id}]此时尚未初始化，无法处理撤成回调")


def on_entrust_withdraw_failed(context: ContextImpl, msg: dict):
    if context.is_inited():
        if msg is None or len(msg) == 0:
            return
        error_info, result_data = covert_message_to_order_class_tuple(msg=msg['msg_content'], data_name="info",
                                                                      data_class=POrderData,
                                                                      return_class=OrderDataImpl)
        if error_info.has_error():
            python_logger.error(f"on_entrust_withdraw_failed收到异常数据,错误原因：{error_info.error_msg}")
            return
        if result_data is None:
            python_logger.error(f"on_entrust_withdraw_failed收到异常数据")
            return
        scheme_ins_code: str = result_data.security_detail_id
        internal_id: str = result_data.internal_id
        revoke_cause: float = result_data.revoke_cause

        python_logger.info(
            f"方案[ID:{context.scheme_id}]-方案明细[ID:{scheme_ins_code}]-子单[ID:{internal_id}], 撤单失败原因[{revoke_cause}]")
        entrust_info = context.entrust_list.update_un_final_state_entrust(new_order_data=result_data)
        if entrust_info is None:
            python_logger.error(f"处理子单委托撤单失败时子单委托列表中找不到子单[ID: {internal_id}]")
            return

        if context.exit_function(method_name="on_order"):
            context.spi_instance.on_order(context, entrust_info, PushType.CANCEL_FAIL)

    else:
        python_logger.error(f"方案[ID: {context.scheme_id}]此时尚未初始化，无法处理撤单失败回调")


def on_snapshot(context: ContextImpl, msg: dict):
    error_info, hq_info = covert_message_to_class_tuple(msg=msg['msg_content'], data_name="hq_infos",
                                                        data_class=PSnapshotData,
                                                        return_class=SnapshotData)
    if error_info.has_error():
        python_logger.error(f"on_snapshot收到异常数据,错误原因：{error_info.error_msg}")
        return
    if hq_info is None:
        python_logger.error(f"on_snapshot收到异常数据")
        return

    stock_key: str = hq_info.security
    HQCacheManage().add_or_update_hq_by_itemkey(item_key=stock_key, hq=hq_info)
    if context is None:

        scheme_id_list: List[int] = HQCacheManage().query_subscribe_by_itemkey(item_key=stock_key)
        for scheme_id in scheme_id_list:
            context = SchemeManage().get_scheme(scheme_id=scheme_id)
            if context is None:
                continue
            context.get_async_message_handler().set_current_scheme_id(scheme_id=scheme_id)
            if hasattr(context.spi_instance, "on_snapshot"):
                context.spi_instance.on_snapshot(context, hq_info)
    else:
        context.spi_instance.on_snapshot(context, hq_info)


def on_position(context: ContextImpl, msg: dict):
    error_info, position_data = covert_message_to_class_tuple(msg=msg['msg_content'], data_name="info",
                                                              data_class=PPositionData,
                                                              return_class=PositionData)
    if error_info.has_error():
        python_logger.error(f"on_position收到异常数据,错误原因：{error_info.error_msg}")
        return
    if position_data is None:
        python_logger.error(f"on_position收到异常数据")
        return
    if context.exit_function(method_name="on_position"):
        context.spi_instance.on_position(context, position_data)


def on_market_duty(context: ContextImpl, msg: dict):
    error_info, market_duty_info = covert_message_to_class_tuple(msg=msg['msg_content'], data_name="info",
                                                                 data_class=PMarketDutyData,
                                                                 return_class=MarketDutyData)
    if error_info.has_error():
        python_logger.error(f"on_market_duty收到异常数据,错误原因：{error_info.error_msg}")
        return
    if market_duty_info is None:
        python_logger.error(f"on_market_duty收到异常数据")
        return
    if context.exit_function(method_name="on_market_duty"):
        context.spi_instance.on_market_duty(context, market_duty_info)


def on_factor(context: ContextImpl, msg: dict):
    error_info, factor_info = covert_message_to_class_tuple(msg=msg['msg_content'], data_name="info",
                                                            data_class=PFactor,
                                                            return_class=Factor)
    if error_info.has_error():
        python_logger.error(f"on_factor收到异常数据,错误原因：{error_info.error_msg}")
        return
    if factor_info is None:
        python_logger.error(f"on_factor收到异常数据")
        return
    key: str = f"{factor_info.security},{factor_info.factor_name}"
    scheme_id_list: List[int] = FactorCacheManageBase().query_subscribe_by_itemkey(item_key=key)

    if context is None:

        for scheme_id in scheme_id_list:
            context = SchemeManage().get_scheme(scheme_id=scheme_id)
            context.get_async_message_handler().set_current_scheme_id(scheme_id=scheme_id)
            if context.exit_function(method_name="on_factor"):
                context.spi_instance.on_factor(context, factor_info)
    else:
        if context.exit_function(method_name="on_factor"):
            context.spi_instance.on_factor(context, factor_info)


def algo_scheme_update(context: ContextImpl, msg: dict):
    error_info, algo_scheme = covert_message_to_p_class_tuple(msg=msg['msg_content'], data_name="info",
                                                              data_class=PAlgoScheme)
    if error_info.has_error():
        python_logger.error(f"algo_scheme_update收到异常数据,错误原因：{error_info.error_msg}")
        return
    if algo_scheme is None:
        python_logger.error(f"algo_scheme_update收到异常数据")
        return
    sub_scheme_manager: SubSchemeManager = SubSchemeManager()
    sub_scheme_manager.update_scheme(algo_scheme)


def algo_scheme_detail_update(context: ContextImpl, msg: dict):
    error_info, algo_scheme_detail = covert_message_to_p_class_tuple(msg=msg['msg_content'], data_name="info",
                                                                     data_class=PAlgoDetail)
    if error_info.has_error():
        python_logger.error(f"algo_scheme_detail_update收到异常数据,错误原因：{error_info.error_msg}")
        return
    if algo_scheme_detail is None:
        python_logger.error(f"algo_scheme_detail_update收到异常数据")
        return
    sub_scheme_manager: SubSchemeManager = SubSchemeManager()
    child_scheme = sub_scheme_manager.get_scheme(algo_scheme_detail.scheme_id)
    if child_scheme is not None:
        scheme_detail = child_scheme.update_detail(algo_scheme_detail)
        if context.exit_function(method_name="on_securitydetail"):
            context.spi_instance.on_securitydetail(context, scheme_detail)


def on_scheme_release(context: ContextImpl, msg: dict):
    scheme_id = context.scheme_id
    from qt_strategy_base.core.cache.scheduler_manage import SchedulerManger
    SchedulerManger().cancel_scheme_job(scheme_id=context.scheme_id)
    SchemeManage().remove_scheme(scheme_id=context.scheme_id)
    from qt_strategy_base.core.common.aglo_function_impl import FunctionImpl
    FunctionImpl.unsub_snapshot()
    FunctionImpl.unsub_factor()
    FunctionImpl.unsub_bond_click_hq()
    FunctionImpl.unsub_xbond()
    FunctionImpl.unsub_intrabank_bond_mm()
    python_logger.info(f"方案[ID:{context.scheme_id}]已释放")
    del context


def on_schedule(context: ContextImpl, msg: dict):
    schedule_job = msg['msg_content']["schedule_job"]
    schedule_job()


def entrust_push(context: ContextImpl, msg: dict):
    error_info, order_data = covert_message_to_order_class_tuple(msg=msg['msg_content'], data_name="info",
                                                                 data_class=POrderData,
                                                                 return_class=OrderDataImpl)
    if error_info.has_error():
        python_logger.error(f"entrust_push收到异常数据,错误原因：{error_info.error_msg}")
        return
    if order_data is None:
        python_logger.error(f"entrust_push收到异常数据")
        return
    error_info, ext_data = covert_message_to_dict_tuple(msg=msg['msg_content'], data_name="ext_info")
    if error_info.has_error():
        python_logger.error(f"entrust_push收到异常额外数据,错误原因：{error_info.error_msg}")
        return
    if ext_data is None:
        python_logger.error(f"entrust_push收到异常额外数据")
        return
    push_type = None
    push_type_int = ext_data.get("push_type", None)
    if push_type_int is not None:
        push_type = covert_to_enum(push_type_int, PushType)

    if context.exit_function(method_name="on_order"):
        context.spi_instance.on_order(context, order_data, push_type)


def deal_push(context: ContextImpl, msg: dict):
    error_info, deal_info = covert_message_to_class_tuple(msg=msg['msg_content'], data_name="info",
                                                          data_class=PTradeData,
                                                          return_class=TradeData)
    if error_info.has_error():
        python_logger.error(f"deal_push收到异常成交数据,错误原因：{error_info.error_msg}")
    if deal_info is None:
        python_logger.error(f"deal_push收到异常数据")
        return
    if context.exit_function(method_name="on_trade"):
        context.spi_instance.on_trade(context, deal_info)


def on_entrust_recovery(context: ContextImpl, msg: dict):
    if context.is_inited():
        error_info, entrust_list = covert_message_to_order_class_list_tuple(msg=msg['msg_content'], data_name="info",
                                                                            data_class=POrderData,
                                                                            return_class=OrderDataImpl)
        if not error_info.has_error() and entrust_list is not None:
            for entrust_info in entrust_list:
                context.recover_entrust(entrust_info=entrust_info)
    else:
        python_logger.warning(f"方案[ID:{context.scheme_id}]此时尚未初始化，无法处理委托恢复请求")


def on_qdbj_push(context: ContextImpl, msg: dict):
    buy_hq_info_list = []
    sell_hq_info_list = []
    base_info_list = {}
    if "buy_info" in msg['msg_content']['body'].keys():
        error_info, buy_hq_info_list = covert_message_to_class_list_tuple(msg=msg['msg_content'], data_name="buy_info",
                                                                          data_class=PQDBJHqInfo,
                                                                          return_class=BondQDBJInfo)
        if error_info.has_error():
            return
    if "sale_info" in msg['msg_content']['body'].keys():
        error_info, sell_hq_info_list = covert_message_to_class_list_tuple(msg=msg['msg_content'],
                                                                           data_name="sale_info",
                                                                           data_class=PQDBJHqInfo,
                                                                           return_class=BondQDBJInfo)
        if error_info.has_error():
            return
    if "base_info" in msg['msg_content']['body'].keys():
        error_info, base_info_list = covert_message_to_dict_tuple(msg=msg['msg_content'], data_name="base_info")
        if error_info.has_error():
            return
    security = base_info_list.get("security", None)
    clear_speed = base_info_list.get("clear_speed", None)
    if security is None or clear_speed is None:
        return
    bond_cj_hq_key = f"{security},{clear_speed}"
    qdbj_hq = {"buy_info": buy_hq_info_list, "sale_info": sell_hq_info_list}
    bond_hq_cache_manage_base: BondHQCacheManageBase = BondHQCacheManageBase()
    bond_hq_cache_manage_base.add_or_update_qdbj_hq_by_itemkey(item_key=bond_cj_hq_key, hq=qdbj_hq)
    scheme_id_list: List[int] = bond_hq_cache_manage_base.query_bond_click_subscribe_by_itemkey(item_key=bond_cj_hq_key)
    for scheme_id in scheme_id_list:
        context = SchemeManage(). get_scheme(scheme_id=scheme_id)
        context.get_async_message_handler().set_current_scheme_id(scheme_id=scheme_id)
        if context.exit_function(method_name="on_bond_click_hq"):
            cj_hq = bond_hq_cache_manage_base.query_cj_hq_by_itemkey(bond_cj_hq_key)
            bond_click_hq = BondClickHq(qdbj_data_info=qdbj_hq, cj_data_info=cj_hq)
            context.spi_instance.on_bond_click_hq(context, bond_click_hq)


def on_cj_push(context: ContextImpl, msg: dict):
    error_info, cj_hq = covert_message_to_p_class_tuple(msg=msg['msg_content'], data_name="info", data_class=PCJHqInfo)
    if cj_hq:
        bond_cj_hq_key = f"{cj_hq.security},{cj_hq.clear_speed}"
        bond_hq_cache_manage_base: BondHQCacheManageBase = BondHQCacheManageBase()
        bond_hq_cache_manage_base.add_or_update_cj_hq_by_itemkey(item_key=bond_cj_hq_key, hq=cj_hq)
        scheme_id_list: List[int] = bond_hq_cache_manage_base.query_bond_click_subscribe_by_itemkey(
            item_key=bond_cj_hq_key)
        for scheme_id in scheme_id_list:
            context = SchemeManage().get_scheme(scheme_id=scheme_id)
            context.get_async_message_handler().set_current_scheme_id(scheme_id=scheme_id)
            if context.exit_function(method_name="on_bond_click_hq"):
                qdbj_hq = bond_hq_cache_manage_base.query_qdbj_hq_by_itemkey(item_key=bond_cj_hq_key)
                bond_click_hq = BondClickHq(qdbj_data_info=qdbj_hq, cj_data_info=cj_hq)
                context.spi_instance.on_bond_click_hq(context, bond_click_hq)


def on_comb_order(context: ContextImpl, msg: dict):
    error_info, order_data = covert_message_to_order_class_tuple(msg=msg['msg_content'], data_name="info",
                                                                 data_class=PCombOrderData,
                                                                 return_class=CombOrderDataImpl)
    if error_info.has_error():
        python_logger.error(f"on_comb_order收到异常数据,错误原因：{error_info.error_msg}")
        return
    if order_data is None:
        python_logger.error(f"on_comb_order收到异常数据")
        return
    error_info, ext_data = covert_message_to_dict_tuple(msg=msg['msg_content'], data_name="ext_info")
    if error_info.has_error():
        python_logger.error(f"on_comb_order收到异常额外数据,错误原因：{error_info.error_msg}")
        return
    if ext_data is None:
        python_logger.error(f"on_comb_order收到异常额外数据")
        return
    push_type = None
    push_type_int = ext_data.get("push_type", None)
    if push_type_int is not None:
        push_type = covert_to_enum(push_type_int, PushType)
    is_fail = False
    if push_type == PushType.ORDER_FAIL:
        current_entrust = context.cb_entrust_list.find_entrust(internal_id=order_data.internal_id)
        if current_entrust is not None and current_entrust.status is not OrderStatus.WASTE:
            is_fail = True
    context.cb_entrust_list.update_entrust(entrust_info=order_data, entrust_type=push_type)
    if not is_fail and context.exit_function(method_name="on_comb_order"):
        context.spi_instance.on_comb_order(context, order_data, push_type)


def on_comb_order_reject(context: ContextImpl, msg: dict):
    error_info, entrust_info = covert_message_to_dict_tuple(msg=msg['msg_content'], data_name="info")
    algo_ordid = entrust_info.get("algo_ordid", "")
    entrust_no = entrust_info.get("entrust_no", 0)
    error_info = entrust_info.get("error_info", "")
    entrust_serial_no_buy = entrust_info.get("entrust_serial_no_buy", 0)
    entrust_serial_no_sale = entrust_info.get("entrust_serial_no_sale", 0)
    current_entrust = context.cb_entrust_list.find_entrust(internal_id=algo_ordid)
    if current_entrust is not None and current_entrust.status is not OrderStatus.WASTE:
        reject_entrust = context.cb_entrust_list.entrust_reject(
            internal_id=algo_ordid, id=entrust_no,
            buy_id=entrust_serial_no_buy,
            sell_id=entrust_serial_no_sale,
            revoke_cause=error_info)
        if reject_entrust is not None and context.exit_function(method_name="on_comb_order"):
            context.spi_instance.on_comb_order(context, reject_entrust, PushType.ORDER_FAIL)


def on_message(context: ContextImpl, msg: dict):
    ext_data = msg['msg_content'].get("ext_data", None)
    if ext_data is not None:
        if context.exit_function(method_name="on_message"):
            context.spi_instance.on_message(context, ext_data)




def on_xbond(context: ContextImpl, msg: dict):
    error_info, xbond_base_info = covert_message_to_p_class_tuple(msg=msg['msg_content'], data_name="info",
                                                                  data_class=PXBondBaseInfo)
    if error_info.has_error():
        python_logger.error(f"on_xbond收到异常数据,错误原因：{error_info.error_msg}")
        return
    xbond_order_dict = {"buy_info": [], "sale_info": []}
    if "buy_info" in msg['msg_content']['body'].keys():
        error_info, buy_hq_info_list = covert_message_to_class_list_tuple(msg=msg['msg_content'], data_name="buy_info",
                                                                          data_class=PXBondOrder,
                                                                          return_class=XBondOrder)
        if error_info.has_error():
            return
        else:
            xbond_order_dict["buy_info"] = buy_hq_info_list
    if "sale_info" in msg['msg_content']['body'].keys():
        error_info, sell_hq_info_list = covert_message_to_class_list_tuple(msg=msg['msg_content'],
                                                                           data_name="sale_info",
                                                                           data_class=PXBondOrder,
                                                                           return_class=XBondOrder)
        if error_info.has_error():
            return
        else:
            xbond_order_dict["sale_info"] = sell_hq_info_list

    hq_info = XBondInfo(xbond_base_info, xbond_order_dict)
    stock_key: str = f"{xbond_base_info.security},{xbond_base_info.clear_speed}"
    xbond_hq_cache_manage_base = XBondHQCacheManageBase()
    xbond_hq_cache_manage_base.add_or_update_hq_by_itemkey(item_key=stock_key, hq=hq_info)
    scheme_id_list: List[int] = xbond_hq_cache_manage_base.query_subscribe_by_itemkey(item_key=stock_key)
    for scheme_id in scheme_id_list:
        context = SchemeManage().get_scheme(scheme_id=scheme_id)
        context.get_async_message_handler().set_current_scheme_id(scheme_id=scheme_id)
        if context is not None and hasattr(context.spi_instance, "on_xbond"):
            context.spi_instance.on_xbond(context, hq_info)


def on_intrabak_bond_mm(context: ContextImpl, msg: dict):
    error_info, intrabak_bond_base_info = covert_message_to_p_class_tuple(msg=msg['msg_content'], data_name="info",
                                                                  data_class=PYHJBondMMInfo)
    if error_info.has_error():
        python_logger.error(f"on_intrabak_bond收到异常数据,错误原因：{error_info.error_msg}")
        return
    intrabak_bond_order_dict = {"buy_info": [], "sale_info": []}
    if "buy_info" in msg['msg_content']['body'].keys():
        error_info, buy_hq_info_list = covert_message_to_class_list_tuple(msg=msg['msg_content'], data_name="buy_info",
                                                                          data_class=PYHJBondMMOrder,
                                                                          return_class=YHJBondMMOrder)
        if error_info.has_error():
            return
        else:
            intrabak_bond_order_dict["buy_info"] = buy_hq_info_list
    if "sale_info" in msg['msg_content']['body'].keys():
        error_info, sell_hq_info_list = covert_message_to_class_list_tuple(msg=msg['msg_content'],
                                                                           data_name="sale_info",
                                                                           data_class=PYHJBondMMOrder,
                                                                           return_class=YHJBondMMOrder)
        if error_info.has_error():
            return
        else:
            intrabak_bond_order_dict["sale_info"] = sell_hq_info_list

    hq_info = YHJBondMMInfo(intrabak_bond_base_info, intrabak_bond_order_dict)
    stock_key: str = f"{intrabak_bond_base_info.security},{intrabak_bond_base_info.clear_speed}"
    intrabak_bond_hq_cache_manage_base = IntrabakBondHqManage()
    intrabak_bond_hq_cache_manage_base.add_or_update_hq_by_itemkey(item_key=stock_key, hq=hq_info)
    scheme_id_list: List[int] = intrabak_bond_hq_cache_manage_base.query_subscribe_by_itemkey(item_key=stock_key)
    for scheme_id in scheme_id_list:
        context = SchemeManage().get_scheme(scheme_id=scheme_id)
        context.get_async_message_handler().set_current_scheme_id(scheme_id=scheme_id)
        if context is not None and hasattr(context.spi_instance, "on_intrabak_bond_mm"):
            context.spi_instance.on_intrabak_bond_mm(context, hq_info)

def on_group_msg_update(context: ContextImpl, msg: dict):
    error_info, group_msg = covert_message_to_p_class_tuple(msg=msg['msg_content'], data_name="info",
                                                                  data_class=PGroupMsgData)
    if error_info.has_error():
        python_logger.error(f"on_group_msg_update收到异常数据,错误原因：{error_info.error_msg}")
        return
    context._group_mange.group_msg_update(group_msg)

FUNCTION_INFO_DICT: Dict[int, FunctionInfo] = {
    FunctionID.CreateScheme.value: FunctionInfo(FunctionID.CreateScheme.value, FunctionType.CREATE.value,
                                                initialize),
    FunctionID.OnSchemePaused.value: FunctionInfo(FunctionID.OnSchemePaused.value, FunctionType.CALLBACK.value,
                                                  on_pause),
    FunctionID.OnSchemeResume.value: FunctionInfo(FunctionID.OnSchemeResume.value, FunctionType.CALLBACK.value,
                                                  on_resume),
    FunctionID.OnSchemeRelease.value: FunctionInfo(FunctionID.OnSchemeRelease.value, FunctionType.CALLBACK.value,
                                                   on_scheme_release),
    FunctionID.OnEntrustReqAccept.value: FunctionInfo(FunctionID.OnEntrustReqAccept.value, FunctionType.CALLBACK.value,
                                                      on_entrust_req_accept),
    FunctionID.OnEntrustReqReject.value: FunctionInfo(FunctionID.OnEntrustReqReject.value, FunctionType.CALLBACK.value,
                                                      on_entrust_req_reject),
    FunctionID.OnEntrustConfirm.value: FunctionInfo(FunctionID.OnEntrustConfirm.value, FunctionType.CALLBACK.value,
                                                    on_entrust_confirm),
    FunctionID.OnTrade.value: FunctionInfo(FunctionID.OnTrade.value, FunctionType.CALLBACK.value, on_trade),
    FunctionID.OnEntrustWaste.value: FunctionInfo(FunctionID.OnEntrustWaste.value, FunctionType.CALLBACK.value,
                                                  on_entrust_waste),
    FunctionID.OnEntrustCancelled.value: FunctionInfo(FunctionID.OnEntrustCancelled.value, FunctionType.CALLBACK.value,
                                                      on_entrust_cancelled),
    FunctionID.OnEntrustWithdrawFailed.value: FunctionInfo(FunctionID.OnEntrustWithdrawFailed.value,
                                                           FunctionType.CALLBACK.value, on_entrust_withdraw_failed),
    FunctionID.OnHqReceive.value: FunctionInfo(FunctionID.OnHqReceive.value, FunctionType.BatchCALLBACK.value,
                                               on_snapshot),

    FunctionID.ScheduleCallBack.value: FunctionInfo(FunctionID.ScheduleCallBack.value,
                                                    FunctionType.INNERCALLBACK.value, on_schedule),
    FunctionID.OnSchemeCancelReq.value: FunctionInfo(FunctionID.OnSchemeCancelReq.value,
                                                     FunctionType.CALLBACK.value, on_cancel),
    FunctionID.GetStockInfo.value: FunctionInfo(FunctionID.GetStockInfo.value, FunctionType.QUERY.value, None),
    FunctionID.GetBondProperty.value: FunctionInfo(FunctionID.GetBondProperty.value, FunctionType.QUERY.value, None),
    FunctionID.GetFutureInfo.value: FunctionInfo(FunctionID.GetFutureInfo.value, FunctionType.QUERY.value, None),
    FunctionID.GetOptionInfo.value: FunctionInfo(FunctionID.GetOptionInfo.value, FunctionType.QUERY.value, None),
    FunctionID.GetOptionInfoByTargetStock.value: FunctionInfo(FunctionID.GetOptionInfoByTargetStock.value,
                                                              FunctionType.QUERY.value, None),
    FunctionID.GetEtfStocks.value: FunctionInfo(FunctionID.GetEtfStocks.value, FunctionType.QUERY.value, None),
    FunctionID.GetEtfInfo.value: FunctionInfo(FunctionID.GetEtfInfo.value, FunctionType.QUERY.value, None),
    FunctionID.GetHqBatch.value: FunctionInfo(FunctionID.GetHqBatch.value, FunctionType.QUERY.value, None),
    FunctionID.GetHoldList.value: FunctionInfo(FunctionID.GetHoldList.value, FunctionType.QUERY.value, None),

    FunctionID.SubHqBatch.value: FunctionInfo(FunctionID.SubHqBatch.value, FunctionType.QUERY.value, None),

    FunctionID.GetOrderIdStart.value: FunctionInfo(FunctionID.GetOrderIdStart.value, FunctionType.QUERY.value, None),
    FunctionID.SystemMessage.value: FunctionInfo(FunctionID.SystemMessage.value, FunctionType.NOTICESERVER, None),
    FunctionID.CancelEntrustBySubID.value: FunctionInfo(FunctionID.CancelEntrustBySubID.value,
                                                        FunctionType.NOTICESERVER, None),
    FunctionID.CallSchemeOverdue.value: FunctionInfo(FunctionID.CallSchemeOverdue.value, FunctionType.QUERY.value,
                                                     None),
    FunctionID.AddHoldSub.value: FunctionInfo(FunctionID.AddHoldSub.value, FunctionType.QUERY.value, None),
    FunctionID.ReleaseHoldSub.value: FunctionInfo(FunctionID.ReleaseHoldSub.value, FunctionType.QUERY.value, None),
    FunctionID.AddEntrustSub.value: FunctionInfo(FunctionID.AddEntrustSub.value, FunctionType.QUERY.value, None),
    FunctionID.ReleaseEntrustSub.value: FunctionInfo(FunctionID.ReleaseEntrustSub.value, FunctionType.QUERY.value,
                                                     None),
    FunctionID.AddDealSub.value: FunctionInfo(FunctionID.AddDealSub.value, FunctionType.QUERY.value, None),
    FunctionID.ReleaseDealSub.value: FunctionInfo(FunctionID.ReleaseDealSub.value, FunctionType.QUERY.value, None),
    FunctionID.AddMktDutySub.value: FunctionInfo(FunctionID.AddMktDutySub.value, FunctionType.QUERY.value, None),
    FunctionID.ReleaseMktDutySub.value: FunctionInfo(FunctionID.ReleaseMktDutySub.value, FunctionType.QUERY.value,
                                                     None),
    FunctionID.AddCbEntrustSub.value: FunctionInfo(FunctionID.AddCbEntrustSub.value, FunctionType.QUERY.value, None),
    FunctionID.ReleaseCbEntrustSub.value: FunctionInfo(FunctionID.ReleaseCbEntrustSub.value, FunctionType.QUERY.value,
                                                       None),
    FunctionID.SchemeStockStatusChange.value: FunctionInfo(FunctionID.SchemeStockStatusChange.value,
                                                           FunctionType.QUERY.value,
                                                           None),
    FunctionID.GetQDBJHq.value: FunctionInfo(FunctionID.GetQDBJHq.value,
                                             FunctionType.QUERY.value,
                                             None),
    FunctionID.GetNEEQHq.value: FunctionInfo(FunctionID.GetNEEQHq.value,
                                             FunctionType.QUERY.value,
                                             None),

    FunctionID.GetCJHq.value: FunctionInfo(FunctionID.GetCJHq.value,
                                           FunctionType.QUERY.value,
                                           None),
    FunctionID.GetKLine.value: FunctionInfo(FunctionID.GetKLine.value,
                                            FunctionType.QUERY.value,
                                            None),
    FunctionID.GetKLineDay.value: FunctionInfo(FunctionID.GetKLineDay.value,
                                               FunctionType.QUERY.value,
                                               None),
    FunctionID.GetAccountFund.value: FunctionInfo(FunctionID.GetAccountFund.value,
                                                  FunctionType.QUERY.value,
                                                  None),
    FunctionID.GetOpenOrders.value: FunctionInfo(FunctionID.GetOpenOrders.value,
                                                 FunctionType.QUERY.value,
                                                 None),
    FunctionID.GetTrades.value: FunctionInfo(FunctionID.GetTrades.value,
                                             FunctionType.QUERY.value,
                                             None),
    FunctionID.UnSubscribeHQ.value: FunctionInfo(FunctionID.UnSubscribeHQ.value,
                                                 FunctionType.QUERY.value,
                                                 None),
    FunctionID.UnSubFactor.value: FunctionInfo(FunctionID.UnSubFactor.value,
                                               FunctionType.QUERY.value,
                                               None),
    FunctionID.GetHisPosition.value: FunctionInfo(FunctionID.GetHisPosition.value,
                                               FunctionType.QUERY.value,
                                               None),
    FunctionID.HoldUpdateCallback.value: FunctionInfo(FunctionID.HoldUpdateCallback.value, FunctionType.CALLBACK.value,
                                                      on_position),
    FunctionID.EntrustPush.value: FunctionInfo(FunctionID.EntrustPush.value, FunctionType.CALLBACK.value,
                                               entrust_push),

    FunctionID.DealPush.value: FunctionInfo(FunctionID.DealPush.value, FunctionType.CALLBACK.value,
                                            deal_push),
    FunctionID.MktDutyPush.value: FunctionInfo(FunctionID.MktDutyPush.value, FunctionType.CALLBACK.value,
                                               on_market_duty),

    FunctionID.StrategyParamModify.value: FunctionInfo(FunctionID.StrategyParamModify.value,
                                                       FunctionType.CALLBACK.value, on_modify),

    FunctionID.EntrustErrorReturn.value: FunctionInfo(FunctionID.EntrustErrorReturn.value, FunctionType.CALLBACK.value,
                                                      on_entrust_req_reject_by_c),
    FunctionID.EntrustRecovery.value: FunctionInfo(FunctionID.EntrustRecovery.value, FunctionType.CALLBACK.value,
                                                   on_entrust_recovery),

    FunctionID.OnFactor.value: FunctionInfo(FunctionID.OnFactor.value, FunctionType.BatchCALLBACK.value,
                                            on_factor),
    FunctionID.AlgoSchemeUpdate.value: FunctionInfo(FunctionID.AlgoSchemeUpdate.value, FunctionType.BatchCALLBACK.value,
                                                    algo_scheme_update),
    FunctionID.AlgoSchemeDetailUpdate.value: FunctionInfo(FunctionID.AlgoSchemeDetailUpdate.value,
                                                          FunctionType.BatchCALLBACK.value,
                                                          algo_scheme_detail_update),
    FunctionID.SubFactor.value: FunctionInfo(FunctionID.SubFactor.value, FunctionType.QUERY.value, None),
    FunctionID.GetFactor.value: FunctionInfo(FunctionID.GetFactor.value, FunctionType.QUERY.value, None),
    FunctionID.GetAlgoScheme.value: FunctionInfo(FunctionID.GetAlgoScheme.value, FunctionType.QUERY.value, None),
    FunctionID.RunAlgoScheme.value: FunctionInfo(FunctionID.RunAlgoScheme.value, FunctionType.QUERY.value, None),
    FunctionID.CancelAlgoScheme.value: FunctionInfo(FunctionID.CancelAlgoScheme.value, FunctionType.QUERY.value, None),
    FunctionID.SubQDBJHq.value: FunctionInfo(FunctionID.SubQDBJHq.value, FunctionType.QUERY.value, None),
    FunctionID.SubCJHq.value: FunctionInfo(FunctionID.SubCJHq.value, FunctionType.QUERY.value, None),
    FunctionID.OnQDBJHqReceive.value: FunctionInfo(FunctionID.OnQDBJHqReceive.value, FunctionType.CALLBACK.value,
                                                   on_qdbj_push),
    FunctionID.OnCJHqReceive.value: FunctionInfo(FunctionID.OnCJHqReceive.value, FunctionType.CALLBACK.value,
                                                 on_cj_push),
    FunctionID.CBEntrustPush.value: FunctionInfo(FunctionID.CBEntrustPush.value, FunctionType.CALLBACK.value,
                                                 on_comb_order),
    FunctionID.OnCBEntrustReqReject.value: FunctionInfo(FunctionID.OnCBEntrustReqReject.value,
                                                        FunctionType.CALLBACK.value,
                                                        on_comb_order_reject),
    FunctionID.ExtMessageCallBack.value: FunctionInfo(FunctionID.ExtMessageCallBack.value,
                                                      FunctionType.INNERCALLBACK.value,
                                                      on_message),
    FunctionID.OnXBondHq.value: FunctionInfo(FunctionID.OnXBondHq.value,
                                             FunctionType.CALLBACK.value,
                                             on_xbond),
    FunctionID.OnIntrabakBondHq.value: FunctionInfo(FunctionID.OnIntrabakBondHq.value,
                                                    FunctionType.CALLBACK.value,
                                                    on_intrabak_bond_mm
                                                    ),
    FunctionID.GetChinabondValuation.value: FunctionInfo(FunctionID.GetChinabondValuation.value, FunctionType.QUERY.value, None),
    FunctionID.BondPricingCalc.value: FunctionInfo(FunctionID.BondPricingCalc.value,
                                                         FunctionType.QUERY.value, None),
    FunctionID.SubIntrabakBondMM.value: FunctionInfo(FunctionID.SubIntrabakBondMM.value,
                                                   FunctionType.QUERY.value, None),
    FunctionID.SubXBondHq.value: FunctionInfo(FunctionID.SubXBondHq.value,
                                                     FunctionType.QUERY.value, None),
    FunctionID.GroupPermissionQRY.value:FunctionInfo(FunctionID.GroupPermissionQRY.value,
                                                     FunctionType.QUERY.value, None),
    FunctionID.UnsubroupCommuntion.value: FunctionInfo(FunctionID.UnsubroupCommuntion.value,
                                                      FunctionType.QUERY.value, None),
    FunctionID.OnGroupMsgUpdate.value: FunctionInfo(FunctionID.OnGroupMsgUpdate.value,
                                                    FunctionType.CALLBACK.value,
                                                    on_group_msg_update
                                                    ),


}


def inner_callback(function_id: int, scheme: ContextImpl, msg):
    function_info: FunctionInfo = FUNCTION_INFO_DICT.get(function_id, None)
    function_info.function(scheme, msg)

