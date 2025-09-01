# -*- coding: utf-8 -*-
from typing import List, Tuple

from qt_strategy_base.core.common import formula_func, python_logger
from qt_strategy_base.core.common.constant import MSGTYPE_ALGOJR_SCHEME_REMAIN, MSGTYPE_ALGOJR_RECOVER_SCHEME
from qt_strategy_base.core.common.public_func import covert_to_enum, covert_order_data_to_dataframe
from qt_strategy_base.core.model.model import PSecurityDetail, PSecurityBaseInfo, PBalanceAndAmount, PCombOrderData
from qt_strategy_base.core.scheme.strategy_cb_order_impl import CombOrderDataImpl
from qt_strategy_base.model.enum import Side, CloseType, Direction, DirectionOut, ControlType, SecurityDetailStatus, \
    Market, ClearSpeed, TradeType, SettleType, ClearType
from qt_strategy_base.model.error_info import ErrorInfo
from qt_strategy_base.core.scheme.strategy_order_impl import OrderDataImpl
from qt_strategy_base.model import CombOrderData, OrderData
from qt_strategy_base.model.security_detail import SecurityDetail
from qt_strategy_base.model.strategy_api_data import SecurityBaseInfo, AccountInfo


class SecurityDetailImpl(SecurityDetail):

    def __init__(self):
        self._id: str = ""  # 证券明细号
        self._security: str = ""  # 证券明细代码
        self._account: AccountInfo = None  # 证券明细代码
        self._side: Side = None  # 委托方向
        self._direction: Direction = None  # 开平方向
        self._close_type: CloseType = None  # 平仓类型
        self._target_value: float = 0  # 目标金额
        self._target_quantity: float = 0  # 目标数量
        self._ctrl_type: ControlType = ControlType.NO_CONTROL  # 按金额控制和按数量控制
        self._limit_price: float = 0  # 价格限制
        self._total_volume: float = 0  # 累计成交数量
        self._total_value: float = 0  # 累计成交金额
        self._order_quantity: float = 0  # 累计委托数量
        self._order_value: float = 0  # 累计委托金额
        self._scheme_stock_status: SecurityDetailStatus = SecurityDetailStatus.RUNNING  # 明细状态

        self._scheme_id = None
        self._is_recovery: bool = False
        self._scheme = None
        self._balance_and_amount: List[PBalanceAndAmount] = []
        self._stock_info: SecurityBaseInfo = None
        self._scheme_stock_storge = {}  # key:str,value:str

    def get_stock_info(self) -> SecurityBaseInfo:
        return self._stock_info

    @staticmethod
    def gather_scheme_stocks_info(scheme_stock_info: PSecurityDetail, stock_info: PSecurityBaseInfo,
                                  scheme,
                                  topic_name: str):

        ret = SecurityDetailImpl()
        ret._scheme = scheme
        ret._raw_data = scheme_stock_info
        ret._account = AccountInfo(investunit_id=scheme_stock_info.investunit_id,
                                   invest_type=scheme_stock_info.invest_type,
                                   portfolio_id=scheme_stock_info.portfolio_id)
        ret._id = scheme_stock_info.id
        python_logger.info(f"正在解析方案明细信息数据[{ret._id}]")
        ret._stock_info = SecurityBaseInfo(stock_info)
        ret._side = covert_to_enum(scheme_stock_info.side, Side)
        ret._direction = covert_to_enum(scheme_stock_info.direction, Direction)
        ret._close_type = covert_to_enum(scheme_stock_info.close_type, CloseType)
        ret._target_value = scheme_stock_info.target_value
        ret._target_quantity = scheme_stock_info.target_quantity
        ret._ctrl_type = covert_to_enum(scheme_stock_info.control_type, ControlType)
        ret._limit_price = scheme_stock_info.limit_price
        python_logger.info(f"主题名称{topic_name}]")
        if topic_name == MSGTYPE_ALGOJR_SCHEME_REMAIN or topic_name == MSGTYPE_ALGOJR_RECOVER_SCHEME:
            ret._is_recovery = True
        ret._total_volume = scheme_stock_info.total_volume
        ret._total_value = scheme_stock_info.total_value
        ret._order_quantity = scheme_stock_info.order_quantity
        ret._order_value = scheme_stock_info.order_value
        ret._security = scheme_stock_info.security
        return ret

    @property
    def id(self) -> str:
        """
        证券明细号
        """
        return self._id

    @property
    def security(self) -> str:
        """
        证券明细代码
        """
        return self._security

    @property
    def side(self) -> Side:
        """
        委托方向
        """
        return self._side

    @property
    def direction(self) -> Direction:
        """
        开平方向
        """
        return self._direction

    @property
    def target_quantity(self) -> float:
        """
        目标数量
        """
        return self._target_quantity

    @property
    def control_type(self) -> ControlType:
        """
        控制类型
        """
        return self._ctrl_type

    @property
    def total_volume(self) -> float:
        """
        累计成交数量
        """
        return self._total_volume

    @property
    def total_value(self) -> float:
        """
        累计成交金额
        """
        return self._total_value

    @property
    def status(self) -> SecurityDetailStatus:
        """
        明细状态
        """
        return self._scheme_stock_status

    @property
    def order_quantity(self) -> float:
        """
        累计委托数量
        """
        return self._order_quantity

    @property
    def order_value(self) -> float:
        """
        累计委托金额
        """
        return self._order_value

    def get_account(self) -> AccountInfo:
        return self._account

    def get_open_order_quantity_and_value(self, side: Side = None, direction: Direction = None) -> (float, float):
        if self._ctrl_type != ControlType.NO_CONTROL:
            if side is None and direction is None:
                side = self._side
                direction = self._direction
            elif side == self._side and direction == self._direction:
                pass
            else:
                return None
        else:
            if side is None and direction is None:
                return None
        balance = 0
        amount = 0
        entrust_direction_out = self.get_entrust_direction_out(entrust_direction=side,
                                                               future_direction=direction)
        for item in self._balance_and_amount:
            if item.entrust_direction_out == entrust_direction_out.value:
                balance += item.entrust_balance
                amount += item.entrust_amount
        return amount, balance

    def get_volume_and_value(self, side: Side = None, direction: Direction = None) -> (float, float):
        if self._ctrl_type != ControlType.NO_CONTROL:
            if side is None and direction is None:
                side = self._side
                direction = self._direction
            elif side == self._side and direction == self._direction:
                pass
            else:
                return None
        else:
            if side is None and direction is None:
                return None
        balance = 0
        amount = 0
        entrust_direction_out = self.get_entrust_direction_out(entrust_direction=side,
                                                               future_direction=direction)
        for item in self._balance_and_amount:
            if item.entrust_direction_out == entrust_direction_out.value:
                balance += item.deal_balance
                amount += item.deal_amount
        return amount, balance

    def get_orders(self):
        internal_order_list: list[OrderData] = self._scheme.entrust_list.get_iterator(self._id)
        return covert_order_data_to_dataframe(order_list=internal_order_list)

    def order(self, price: float, quantity: float, side: Side = None, direction: Direction = None,
              close_type: CloseType = None, remark: str = "") -> Tuple[ErrorInfo, OrderData]:

        error_info = ErrorInfo()
        stock_code, market_no = self._security.split('.')

        if self._ctrl_type is not ControlType.NO_CONTROL:  # 控量控方向
            if side is not None or direction is not None:
                error_info.set_error_value(error_msg="该明细是控制数量和方向的，报单入参填写错误！")
                return error_info, None
            else:
                side = self._side
                direction = self._direction
                close_type = self._close_type
        else:
            if side is None:
                error_info.set_error_value(error_msg="该明细不存在委托方向信息，报单入参填写错误！")
                return error_info, None

        if market_no == Market.XSGE.value or market_no == Market.XINE.value:
            if direction == Direction.CLOSE and close_type is None:
                error_info.set_error_value(error_msg="上期所和能交所平仓时平仓类型（close_type）需要填写！")
                return error_info, None
        else:
            close_type = None

        # 处理委托请求
        entrust: OrderData = self._scheme.entrust_list.create_limit_entrust(price=price, quantity=quantity,
                                                                            side=side,
                                                                            direction=direction,
                                                                            close_type=close_type,
                                                                            scheme_ins_code=self._id,
                                                                            remark=remark,
                                                                            security=self._security
                                                                            )
        if entrust is not None:
            self.on_entrust_req(entrust_amount=entrust.quantity, entrust_price=entrust.price,
                                side=side, direction=direction)
            self._scheme.send_entrust_req(entrust_info=entrust, clear_speed=None, entrust_type=0,
                                          is_nicked=False, counterparty_order_id='',
                                          trade_type=None)
        return error_info, entrust

    def click_order(self, price: float, quantity: float, side: Side = None, clear_speed: ClearSpeed = None,
                    is_nicked: bool = True, counterparty_order_id: str = "", trade_type: TradeType = TradeType.DEFAULT,
                    remark: str = "") -> Tuple[ErrorInfo, OrderData]:
        error_info = ErrorInfo()
        stock_code, market_no = self._security.split('.')
        if self._ctrl_type is not ControlType.NO_CONTROL:  # 控量控方向
            if side is not None:
                error_info.set_error_value(error_msg="该明细是控制数量和方向的，报单入参填写错误！")
                return error_info, None
            else:
                side = self._side

        else:
            if side is None:
                error_info.set_error_value(error_msg="该明细不存在委托方向信息，报单入参填写错误！")
                return error_info, None

        direction = None
        close_type = None

        # 处理委托请求
        entrust: OrderDataImpl = self._scheme.entrust_list.create_limit_entrust(price=price, quantity=quantity,
                                                                                side=side,
                                                                                direction=direction,
                                                                                close_type=close_type,
                                                                                scheme_ins_code=self._id,
                                                                                remark=remark,
                                                                                security=self._security
                                                                                )
        entrust.set_is_nicked(is_nicked)
        entrust.set_clear_speed(clear_speed)
        entrust.set_counterparty_order_id(counterparty_order_id)
        if entrust is not None:
            self.on_entrust_req(entrust_amount=entrust.quantity, entrust_price=entrust.price,
                                side=side, direction=direction)
            self._scheme.send_entrust_req(entrust_info=entrust, clear_speed=clear_speed, entrust_type=1,
                                          is_nicked=is_nicked, counterparty_order_id=counterparty_order_id,
                                          trade_type=trade_type)
        return error_info, entrust

    def comb_order(self, buy_quantity: float, sell_quantity: float, buy_price: float, sell_price: float,
                   buy_direction: Direction = None, sell_direction: Direction = None, buy_close_type: CloseType = None,
                   sell_close_type: CloseType = None, clear_speed: ClearSpeed = None,
                   replace_order_id: str = "", remark: str = "", is_nicked=True) -> Tuple[ErrorInfo, CombOrderData]:
        error_info = ErrorInfo()
        # 校验通过 正常委托
        entrust_info = CombOrderDataImpl()
        entrust_info.create_comb_entrust(security=self._security, scheme_id=self._scheme_id,
                                         security_detail_id=self._id,
                                         buy_quantity=buy_quantity, sell_quantity=sell_quantity, buy_price=buy_price,
                                         sell_price=sell_price, buy_direction=buy_direction,
                                         sell_direction=sell_direction, buy_close_type=buy_close_type,
                                         sell_close_type=sell_close_type, remark=remark)
        self._scheme.cb_entrust_list.insert_entrust(entrust_info)
        self._scheme.send_cb_entrust_req(entrust_info=entrust_info, replace_order_id=replace_order_id,
                                         is_nicked=is_nicked, clear_speed=clear_speed, entrust_type=0,
                                         expire_time=0, iceberg_quantity=0,
                                         settle_type=None, clear_type=None)

        return error_info, entrust_info

    def intrabank_comb_order(self, buy_quantity: float, sell_quantity: float, buy_price: float, sell_price: float,
                             expire_time: int, iceberg_quantity: float, settle_type: SettleType, clear_type: ClearType,
                             remark: str = "", is_nicked=True) -> Tuple[ErrorInfo, CombOrderData]:
        error_info = ErrorInfo()
        # 校验通过 正常委托
        entrust_info = CombOrderDataImpl()
        entrust_info.create_comb_entrust(security=self._security, scheme_id=self._scheme_id,
                                         security_detail_id=self._id,
                                         buy_quantity=buy_quantity, sell_quantity=sell_quantity, buy_price=buy_price,
                                         sell_price=sell_price, buy_direction=None,
                                         sell_direction=None, buy_close_type=None,
                                         sell_close_type=None, remark=remark)
        self._scheme.cb_entrust_list.insert_entrust(entrust_info)
        self._scheme.send_cb_entrust_req(entrust_info=entrust_info, replace_order_id=0,
                                         is_nicked=is_nicked, clear_speed=None, entrust_type=1,
                                         expire_time=expire_time, iceberg_quantity=iceberg_quantity,
                                         settle_type=settle_type, clear_type=clear_type)

        return error_info, entrust_info

    def set_scheme_stock_status(self, stock_status: SecurityDetailStatus):
        b_change_flag = False
        if stock_status == SecurityDetailStatus.CANCELLED:
            b_change_flag = self._scheme_stock_status == SecurityDetailStatus.CANCELLING
        elif stock_status == SecurityDetailStatus.CANCELLING or stock_status == SecurityDetailStatus.EXPIRED or stock_status == SecurityDetailStatus.FINISHED:
            b_change_flag = (
                    self._scheme_stock_status == SecurityDetailStatus.PAUSED or self._scheme_stock_status == SecurityDetailStatus.RUNNING)
        elif stock_status == SecurityDetailStatus.PAUSED:
            b_change_flag = self._scheme_stock_status == SecurityDetailStatus.RUNNING
        elif stock_status == SecurityDetailStatus.RUNNING:
            b_change_flag = self._scheme_stock_status == SecurityDetailStatus.PAUSED
        else:
            pass
        if b_change_flag:
            self._scheme_stock_status = stock_status
        return b_change_flag

    def get_entrust_direction_out(self, entrust_direction: Side, future_direction: Direction) -> DirectionOut:
        entrust_direction_out = DirectionOut.NONE
        if future_direction is not None:
            if entrust_direction == Side.BUY:
                if future_direction == Direction.OPEN:
                    entrust_direction_out = DirectionOut.BUY_OPEN
                elif future_direction == Direction.CLOSE:
                    entrust_direction_out = DirectionOut.BUY_CLOSE
            elif entrust_direction == Side.SELL:
                if future_direction == Direction.OPEN:
                    entrust_direction_out = DirectionOut.SALE_OPEN
                elif future_direction == Direction.CLOSE:
                    entrust_direction_out = DirectionOut.SALE_CLOSE

        else:  # 现货类型
            if entrust_direction == Side.BUY:
                entrust_direction_out = DirectionOut.BUY
            elif entrust_direction == Side.SELL:
                entrust_direction_out = DirectionOut.SALE
        return entrust_direction_out

    def on_entrust_req_reject(self, entrust_info: OrderData, entrust_amount: float, entrust_price: float):
        if self._side is not None:
            self._order_value -= formula_func.calc_balance(stock_info=self._stock_info,
                                                           price=entrust_price, amount=entrust_amount)
            self._order_quantity -= entrust_amount
        else:
            if entrust_info is not None:
                entrust_balance = -formula_func.calc_balance(stock_info=self._stock_info,
                                                             price=entrust_price, amount=entrust_amount)
                entrust_direction_out = self.get_entrust_direction_out(entrust_info.side,
                                                                       entrust_info.direction)
                self._change_entrust_balance_and_amount(entrust_direction_out=entrust_direction_out,
                                                        balance=entrust_balance,
                                                        amount=-entrust_amount)

    def on_trade(self, entrust_info: OrderData, total_volume: float, total_value: float):
        if self._side is not None:
            self._total_volume += total_volume
            self._total_value += total_value
        else:
            if entrust_info is not None:
                entrust_direction_out = self.get_entrust_direction_out(entrust_info.side,
                                                                       entrust_info.direction)
                self._change_deal_balance_and_amount(entrust_direction_out=entrust_direction_out,
                                                     balance=total_value, amount=total_volume)

    def on_entrust_filled(self, entrust_info: OrderData, un_filled_amount: float, un_filled_balance: float):
        if self._side is not None:
            self._order_quantity -= un_filled_amount
            self._order_value -= un_filled_balance
        else:
            if entrust_info is not None:
                entrust_direction_out = self.get_entrust_direction_out(entrust_info.side,
                                                                       entrust_info.direction)
                self._change_entrust_balance_and_amount(entrust_direction_out=entrust_direction_out,
                                                        balance=-un_filled_balance,
                                                        amount=-un_filled_amount)

    def on_entrust_cancelled(self, entrust_info: OrderData, cancelled_amount: float, cancelled_balance: float):
        if self._side is not None:
            self._order_value -= cancelled_balance
            self._order_quantity -= cancelled_amount
        else:
            if entrust_info is not None:
                entrust_direction_out = self.get_entrust_direction_out(entrust_info.side,
                                                                       entrust_info.direction)
                self._change_entrust_balance_and_amount(entrust_direction_out=entrust_direction_out,
                                                        balance=-cancelled_balance,
                                                        amount=-cancelled_amount)

    def on_entrust_waste(self, entrust_info: OrderData, entrust_amount: float, entrust_price: float):
        if self._side is not None:
            self._order_value -= formula_func.calc_balance(stock_info=self._stock_info,
                                                           price=entrust_price, amount=entrust_amount)
            self._order_quantity -= entrust_amount
        else:
            if entrust_info is not None:
                balance = -formula_func.calc_balance(stock_info=self._stock_info,
                                                     price=entrust_price, amount=entrust_amount)
                entrust_direction_out = self.get_entrust_direction_out(entrust_info.side,
                                                                       entrust_info.direction)
                self._change_entrust_balance_and_amount(entrust_direction_out=entrust_direction_out, balance=balance,
                                                        amount=-entrust_amount)

    def on_entrust_req(self, entrust_amount: float, entrust_price: float, side: Side,
                       direction: Direction):

        entrust_direction_out = self.get_entrust_direction_out(entrust_direction=side,
                                                               future_direction=direction)
        python_logger.info("委托请求修改维护数据")
        balance = formula_func.calc_balance(stock_info=self._stock_info, price=entrust_price,
                                            amount=entrust_amount)
        self._order_value += balance
        self._order_quantity += entrust_amount
        self._change_entrust_balance_and_amount(entrust_direction_out=entrust_direction_out, balance=balance,
                                                amount=entrust_amount)

    def _change_deal_balance_and_amount(self, entrust_direction_out: DirectionOut, balance: float,
                                        amount: float) -> bool:

        found = False
        for item in self._balance_and_amount:
            if item.entrust_direction_out == entrust_direction_out.value:
                item.deal_amount += amount
                item.deal_balance += balance
                found = True
                python_logger.debug(f"方向:{entrust_direction_out.value},数量：{amount},金额：{balance}")
                break
        if not found:
            balance_and_amount = PBalanceAndAmount(entrust_direction_out=entrust_direction_out.value, entrust_amount=0,
                                                   entrust_balance=0, deal_amount=amount,
                                                   deal_balance=balance)
            self._balance_and_amount.append(balance_and_amount)
            python_logger.debug(f"方向:{entrust_direction_out.value},数量：{amount},金额：{balance}")

        return True

    def _change_entrust_balance_and_amount(self, entrust_direction_out: DirectionOut, balance: float,
                                           amount: float) -> bool:
        found = False
        for item in self._balance_and_amount:
            if item.entrust_direction_out == entrust_direction_out.value:
                item.entrust_amount += amount
                item.entrust_balance += balance
                found = True
                python_logger.debug(f"方向:{entrust_direction_out.value},数量：{amount},金额：{balance}")
                break
        if not found:
            balance_and_amount = PBalanceAndAmount(entrust_direction_out=entrust_direction_out.value,
                                                   entrust_amount=amount,
                                                   entrust_balance=balance, deal_amount=0, deal_balance=0)
            self._balance_and_amount.append(balance_and_amount)
            python_logger.debug(f"方向:{entrust_direction_out.value},数量：{amount},金额：{balance}")

        return True

    def recover_balance_and_amount(self, balance_and_amount: List[PBalanceAndAmount]):
        self._balance_and_amount = balance_and_amount
