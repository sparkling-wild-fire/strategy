# -*- coding: utf-8 -*-
import datetime

from qt_strategy_base import covert_to_enum, Direction, OrderStatus, InvestType, CloseType, ClearSpeed
from qt_strategy_base.core.common.public_func import get_order_id
from qt_strategy_base.core.model.model import PCombOrderData
from qt_strategy_base.model.comb_order import CombOrderData


class CombOrderDataImpl(CombOrderData):

    def __init__(self):
        self._security: str = ""
        self._id: int = 0
        self._datetime = None
        self._status: OrderStatus = None
        self._buy_price: float = 0
        self._sell_price: float = 0
        self._buy_quantity: float = 0
        self._sell_quantity: float = 0
        self._buy_cancel_quantity: float = 0
        self._sell_cancel_quantity: float = 0
        self._buy_direction: Direction = None
        self._sell_direction: Direction = None
        self._buy_close_type: CloseType = None
        self._sell_close_type: CloseType = None
        self._buy_id: int = 0
        self._sell_id: int = 0
        self._buy_status: OrderStatus = None
        self._sell_status: OrderStatus = None
        self._internal_id: str = ""
        self._invest_type: InvestType = None
        self._revoke_cause: str = ""
        self._investunit_id: int = 0
        self._portfolio_id: int = 0
        self._buy_filled_quantity: float = 0
        self._sell_filled_quantity: float = 0
        self._buy_filled_value: float = 0
        self._sell_filled_value: float = 0
        self._remark: str = ""
        self._scheme_id: int = 0
        self._security_detail_id: str = ""
        self._operator_no: int = 0

    @property
    def security(self) -> str:
        """
        代码
        """
        return self._security

    @property
    def id(self) -> int:
        """
        委托编号
        """
        return self._id

    @property
    def datetime(self) -> datetime:
        """
        委托时间
        """
        if self._datetime is None:
            return None
        else:
            return datetime.datetime.fromtimestamp(self._datetime)

    @property
    def status(self) -> OrderStatus:
        """
        委托状态
        """
        return self._status

    @property
    def buy_price(self) -> float:
        """
        买方向委托价格
        """
        return self._buy_price

    @property
    def sell_price(self) -> float:
        """
        卖方向委托价格
        """
        return self._sell_price

    @property
    def buy_quantity(self) -> float:
        """
        买方向委托数量
        """
        return self._buy_quantity

    @property
    def sell_quantity(self) -> float:
        """
        卖方向委托数量
        """
        return self._sell_quantity

    @property
    def buy_cancel_quantity(self) -> float:
        """
        买方向撤单数量
        """
        return self._buy_cancel_quantity

    @property
    def sell_cancel_quantity(self) -> float:
        """
        卖方向撤单数量
        """
        return self._sell_cancel_quantity

    @property
    def buy_direction(self) -> Direction:
        """
        买方向的开平方向
        """
        return self._buy_direction

    @property
    def sell_direction(self) -> Direction:
        """
        卖方向的开平方向
        """
        return self._sell_direction

    @property
    def buy_id(self) -> int:
        """
        买方向委托序号(外部委托)
        """
        return self._buy_id

    @property
    def sell_id(self) -> int:
        """
        卖方向委托序号(外部委托)
        """
        return self._sell_id

    @property
    def buy_status(self) -> OrderStatus:
        """
        买方向委托状态
        """
        return self._buy_status

    @property
    def sell_status(self) -> OrderStatus:
        """
        卖方向委托状态
        """
        return self._sell_status

    @property
    def internal_id(self) -> str:
        """
        内部委托号
        """
        return self._internal_id

    @property
    def invest_type(self) -> InvestType:
        """
        投资类型
        """
        return self._invest_type

    @property
    def revoke_cause(self) -> str:
        """
        废单原因
        """
        return self._revoke_cause

    def set_revoke_cause(self, revoke_cause: str):
        self._revoke_cause = revoke_cause

    @property
    def investunit_id(self) -> int:
        """
        账户 ID
        """
        return self._investunit_id

    @property
    def portfolio_id(self) -> int:
        """
        投资组合 ID
        """
        return self._portfolio_id

    @property
    def buy_filled_quantity(self) -> float:
        """
        买方向成交数量
        """
        return self._buy_filled_quantity

    @property
    def sell_filled_quantity(self) -> float:
        """
        卖方向成交数量
        """
        return self._sell_filled_quantity

    @property
    def buy_filled_value(self) -> float:
        """
        买方向成交金额
        """
        return self._buy_filled_value

    @property
    def sell_filled_value(self) -> float:
        """
        卖方向成交金额
        """
        return self._sell_filled_value

    @property
    def remark(self) -> str:
        """
        备注消息
        """
        return self._remark

    @property
    def scheme_id(self) -> int:
        """
        方案号
        """
        return self._scheme_id

    @property
    def security_detail_id(self) -> str:
        """
        方案明细号
        """
        return self._security_detail_id

    @property
    def operator_no(self) -> int:
        """
        操作员号
        """
        return self._operator_no

    def set_value(self, entrust_info: PCombOrderData):
        self._security: str = entrust_info.security
        self._id: int = entrust_info.id
        self._datetime = entrust_info.datetime
        self._status: OrderStatus = covert_to_enum(entrust_info.status, OrderStatus)
        self._buy_price: float = entrust_info.buy_price
        self._sell_price: float = entrust_info.sell_price
        self._buy_quantity: float = entrust_info.buy_quantity
        self._sell_quantity: float = entrust_info.sell_quantity
        self._buy_cancel_quantity: float = entrust_info.buy_cancel_quantity
        self._sell_cancel_quantity: float = entrust_info.sell_cancel_quantity
        self._buy_direction: Direction = covert_to_enum(entrust_info.buy_direction, Direction)
        self._sell_direction: Direction = covert_to_enum(entrust_info.sell_direction, Direction)
        self._buy_close_type: CloseType = covert_to_enum(entrust_info.buy_close_type, CloseType)
        self._sell_close_type: CloseType = covert_to_enum(entrust_info.sell_close_type, CloseType)
        self._buy_id: int = entrust_info.buy_id
        self._sell_id: int = entrust_info.sell_id
        self._buy_status: OrderStatus = covert_to_enum(entrust_info.buy_status, OrderStatus)
        self._sell_status: OrderStatus = covert_to_enum(entrust_info.sell_status, OrderStatus)
        self._internal_id: str = entrust_info.internal_id
        self._invest_type: InvestType = covert_to_enum(entrust_info.invest_type, OrderStatus)
        self._revoke_cause: str = entrust_info.revoke_cause
        self._investunit_id: int = entrust_info.investunit_id
        self._portfolio_id: int = entrust_info.portfolio_id
        self._buy_filled_quantity: float = entrust_info.buy_filled_quantity
        self._sell_filled_quantity: float = entrust_info.sell_filled_quantity
        self._buy_filled_value: float = entrust_info.buy_filled_value
        self._sell_filled_value: float = entrust_info.sell_filled_value
        self._remark: str = entrust_info.remark
        self._scheme_id = entrust_info.scheme_id
        self._security_detail_id = entrust_info.security_detail_id
        self._operator_no: int = entrust_info.operator_no

    def create_comb_entrust(self, security: str, scheme_id: int, security_detail_id: str, buy_quantity: float,
                            sell_quantity: float, buy_price: float, sell_price: float,
                            buy_direction: Direction = None, sell_direction: Direction = None,
                            buy_close_type: CloseType = None,
                            sell_close_type: CloseType = None, remark: str = ""):
        self._security: str = security
        self._buy_price: float = buy_price
        self._sell_price: float = sell_price
        self._buy_quantity: float = buy_quantity
        self._sell_quantity: float = sell_quantity
        self._buy_direction: Direction = buy_direction
        self._sell_direction: Direction = sell_direction
        self._buy_close_type: CloseType = buy_close_type
        self._sell_close_type: CloseType = sell_close_type
        self._status: OrderStatus = OrderStatus.UNREPORT
        self._buy_status: OrderStatus = OrderStatus.UNREPORT
        self._sell_status: OrderStatus = OrderStatus.UNREPORT
        self._internal_id: str = get_order_id()
        self._remark: str = remark
        self._scheme_id: int = scheme_id
        self._security_detail_id: str = security_detail_id

    def update_comb_entrust(self, revoke_cause: str, id: int = 0, buy_id: int = 0, sell_id: int = 0):
        if id != 0:
            self._id = id
        if buy_id != 0:
            self._buy_id = buy_id
        if sell_id != 0:
            self._sell_id = sell_id
        self._revoke_cause = revoke_cause
        self._status = OrderStatus.WASTE
        self._buy_status = OrderStatus.WASTE
        self._sell_status = OrderStatus.WASTE
