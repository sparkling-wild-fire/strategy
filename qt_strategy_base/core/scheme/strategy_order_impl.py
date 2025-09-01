# -*- coding: utf-8 -*-
import datetime

from qt_strategy_base.core.common.public_func import get_mill, covert_to_enum
from  qt_strategy_base.common.math_impl import  feq,fls
from qt_strategy_base.core.model.model import POrderData
from qt_strategy_base.model.enum import Side, Direction, CloseType, OrderStatus, InvestType, TradeType, ClearSpeed
from qt_strategy_base.model.order import OrderData


class OrderDataImpl(OrderData):

    def __init__(self):

        self._id: int = 0  # 委托编号
        self._security: str = ""  # 代码
        self._datetime = None  # 委托时间
        self._price: float = 0.0  # 委托价格
        self._quantity: float = 0.0  # 委托数量
        self._side: Side = None  # 委托方向
        self._direction: Direction = None  # 开平方向
        self._close_type: CloseType = None  # 平仓类型
        self._status: OrderStatus = None  # 委托状态
        self._invest_type: InvestType = None  # 投资类型
        self._internal_id: str = ""  # 内部委托号
        self._revoke_cause: str = ""  # 委托拒绝/委托撤废等原因
        self._cancel_quantity: int = 0  # 撤单数量
        self._investunit_id: int = 0  # 投资单元ID
        self._portfolio_id: int = 0  # 投资组合 ID
        self._filled_value: float = 0.0  # 成交金额
        self._filled_quantity: int = 0  # 成交数量
        self._remark: str = ""  # 备注
        self._scheme_id: int = 0  # 方案号
        self._security_detail_id: str = ""  # 方案明细号
        self._operator_no: int = 0  # 操作员号

        self._cancel_value: float = 0.0  # 撤单金额
        self._last_cancel_time = 0  # 最新撤单时间
        self._is_limit: bool = True  # 是否为限价单
        self._cancel_type = 0  # 撤单状态  0 没有撤单  1正在撤单   2撤废 3 撤成（撤成即删掉，该状态可忽略不计）

        self._is_nicked: bool = True  # 是否匿名
        self._clear_speed: ClearSpeed = None  # 清算速度
        self._counterparty_order_id: str = ""  # 对手方报价编号

    @property
    def id(self) -> int:
        """
        委托编号
        """
        return self._id

    def set_id(self, id: int):
        self._id = id

    @property
    def security(self) -> str:
        """
        代码
        """
        return self._security

    def set_security(self, security: str):
        self._security = security

    @property
    def datetime(self) -> datetime:
        """
        委托时间
        """
        if self._datetime is None:
            return None
        else:
            return datetime.datetime.fromtimestamp(self._datetime)

    def set_datetime(self, datetime: str):
        self._datetime = datetime

    @property
    def price(self) -> float:
        """
        委托价格
        """
        return self._price

    def set_price(self, price: float):
        self._price = price

    @property
    def quantity(self) -> float:
        """
        委托数量
        """
        return self._quantity

    def set_quantity(self, quantity: float):
        self._quantity = quantity

    @property
    def side(self) -> Side:
        """
        委托方向
        """
        return self._side

    def set_side(self, side: Side):
        self._side = side

    @property
    def direction(self) -> Direction:
        """
        开平方向
        """
        return self._direction

    def set_direction(self, direction: Direction):
        self._direction = direction

    @property
    def close_type(self) -> CloseType:
        """
        平仓类型
        """
        return self._close_type

    def set_close_type(self, close_type: CloseType):
        self._close_type = close_type

    @property
    def status(self) -> OrderStatus:
        """
        委托状态
        """
        return self._status

    def set_status(self, status: OrderStatus):
        self._status = status

    @property
    def invest_type(self) -> InvestType:
        """
        投资类型
        """
        return self._invest_type

    def set_invest_type(self, invest_type: InvestType):
        self._invest_type = invest_type

    @property
    def internal_id(self) -> str:
        """
        内部委托号
        """
        return self._internal_id

    def set_internal_id(self, internal_id: str):
        self._internal_id = internal_id

    @property
    def revoke_cause(self) -> str:
        """
        委托拒绝/委托撤废等原因
        """
        return self._revoke_cause

    def set_revoke_cause(self, revoke_cause: str):
        self._revoke_cause = revoke_cause

    @property
    def cancel_quantity(self) -> float:
        """
        撤单数量
        """
        return self._cancel_quantity

    def set_cancel_quantity(self, cancel_quantity: float):
        self._cancel_quantity = cancel_quantity

    def get_cancel_value(self) -> float:
        """
        撤单金额
        """
        return self._cancel_value

    @property
    def investunit_id(self) -> int:
        """
        投资单元ID
        """
        return self._investunit_id

    def set_investunit_id(self, investunit_id: int):
        self._investunit_id = investunit_id

    @property
    def portfolio_id(self) -> int:
        """
        投资组合 ID
        """
        return self._portfolio_id

    def set_portfolio_id(self, portfolio_id: int):
        self._portfolio_id = portfolio_id

    @property
    def filled_quantity(self) -> int:
        """
        成交数量
        """
        return self._filled_quantity

    def set_filled_quantity(self, filled_quantity: int):
        self._filled_quantity = filled_quantity
        if feq(self._filled_quantity,self._quantity):
            self._status= OrderStatus.FILLED
        if  fls(self._filled_quantity,self._quantity) and self._filled_quantity>0 and feq( self._cancel_quantity,0):
            self._status=OrderStatus.PARTFILLED

    @property
    def filled_value(self) -> float:
        """
        成交金额
        """
        return self._filled_value

    def set_filled_value(self, filled_value: float):
        self._filled_value = filled_value

    @property
    def remark(self) -> str:
        """
        备注
        """
        return self._remark

    def set_remark(self, remark: str):
        self._remark = remark

    @property
    def scheme_id(self) -> int:
        """
        方案号
        """
        return self._scheme_id

    def set_scheme_id(self, scheme_id: str):
        self._scheme_id = scheme_id

    @property
    def security_detail_id(self) -> str:
        """
        方案明细号
        """
        return self._security_detail_id

    def set_security_detail_id(self, security_detail_id: str):
        self._security_detail_id = security_detail_id

    @property
    def operator_no(self) -> int:
        """
        操作员号
        """
        return self._operator_no

    def set_operator_no(self, operator_no: int):
        self._operator_no = operator_no

    def is_limit(self) -> bool:
        return self._is_limit

    def set_limit(self, is_limit: bool):
        self._is_limit = is_limit

    def get_cancel_type(self) -> int:
        return self._cancel_type

    def set_cancel_type(self, cancel_type: int):
        self._cancel_type = cancel_type

    def update_last_cancel_time(self):
        self._last_cancel_time = get_mill()

    def get_last_cancel_time(self) -> int:
        return self._last_cancel_time

    @property
    def is_nicked(self) -> bool:
        """
        是否匿名
        """
        return self._is_nicked

    def set_is_nicked(self, is_nicked: bool):
        self._is_nicked = is_nicked

    @property
    def clear_speed(self) -> ClearSpeed:
        """
        是否匿名
        """
        return self._clear_speed

    def set_clear_speed(self, clear_speed: ClearSpeed):
        self._clear_speed = clear_speed

    @property
    def counterparty_order_id(self) -> str:
        """
        对手方报价编号
        """
        return self._counterparty_order_id

    def set_counterparty_order_id(self, counterparty_order_id: str):
        self._counterparty_order_id = counterparty_order_id

    def set_value(self, entrust_info: POrderData):
        self._id: int = entrust_info.id  # 委托编号
        self._security: str = entrust_info.security  # 代码
        self._datetime: str = entrust_info.datetime  # 委托时间
        self._price: float = entrust_info.price  # 委托价格
        self._quantity: float = entrust_info.quantity  # 委托数量
        self._side: Side = covert_to_enum(entrust_info.side, Side)  # 委托方向
        self._direction: Direction = covert_to_enum(entrust_info.direction, Direction)  # 开平方向
        self._close_type: CloseType = covert_to_enum(entrust_info.close_type, CloseType)  # 平仓类型
        self._status: OrderStatus = covert_to_enum(entrust_info.status, OrderStatus)  # 委托状态
        self._invest_type: InvestType = covert_to_enum(entrust_info.invest_type, InvestType)  # 投资类型
        self._internal_id: str = entrust_info.internal_id  # 内部委托号
        self._revoke_cause: str = entrust_info.revoke_cause  # 委托拒绝/委托撤废等原因
        self._cancel_quantity: float = entrust_info.cancel_quantity  # 撤单数量
        self._cancel_value: float = entrust_info.cancel_value  # 撤单数量
        self._investunit_id: int = entrust_info.investunit_id  # 投资单元ID
        self._portfolio_id: int = entrust_info.portfolio_id  # 投资组合 ID
        self._filled_quantity: float = entrust_info.filled_quantity  # 成交数量
        self._filled_value: float = entrust_info.filled_value  # 成交金额
        self._remark: str = entrust_info.remark  # 备注
        self._scheme_id: int = entrust_info.scheme_id  # 方案号
        self._security_detail_id: str = entrust_info.security_detail_id  # 方案明细号
        self._operator_no: int = entrust_info.operator_no  # 操作员号
        self._is_nicked: bool = True if entrust_info.is_nicked else False
        self._clear_speed: ClearSpeed = covert_to_enum(entrust_info.clear_speed, ClearSpeed)
        self._counterparty_order_id = entrust_info.counterparty_order_id
