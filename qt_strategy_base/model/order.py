# -*- coding: utf-8 -*-

from qt_strategy_base.core.model.base import BaseObject

from qt_strategy_base.model.enum import Side, Direction, CloseType, OrderStatus, InvestType, ClearSpeed, TradeType


class OrderData(BaseObject):
    @property
    def id(self) -> int:
        """
        委托编号
        """
        pass

    @property
    def security(self) -> str:
        """
        代码
        """
        pass

    @property
    def datetime(self) -> str:
        """
        委托时间
        """
        pass

    @property
    def price(self) -> float:
        """
        委托价格
        """
        pass

    @property
    def quantity(self) -> float:
        """
        委托数量
        """
        pass

    @property
    def side(self) -> Side:
        """
        委托方向
        """
        pass

    @property
    def direction(self) -> Direction:
        """
        开平方向
        """
        pass

    @property
    def close_type(self) -> CloseType:
        """
        平仓类型
        """
        pass

    @property
    def status(self) -> OrderStatus:
        """
        委托状态
        """
        pass

    @property
    def invest_type(self) -> InvestType:
        """
        投资类型
        """
        pass

    @property
    def internal_id(self) -> str:
        """
        内部委托号
        """
        pass

    @property
    def revoke_cause(self) -> str:
        """
        委托拒绝/委托撤废等原因
        """
        pass

    @property
    def cancel_quantity(self) -> float:
        """
        撤单数量
        """
        pass

    @property
    def investunit_id(self) -> int:
        """
        投资单元ID
        """
        pass

    @property
    def portfolio_id(self) -> int:
        """
        投资组合 ID
        """
        pass

    @property
    def filled_quantity(self) -> int:
        """
        成交数量
        """
        pass

    @property
    def filled_value(self) -> float:
        """
        成交金额
        """
        pass

    @property
    def remark(self) -> str:
        """
        备注
        """
        pass

    @property
    def scheme_id(self) -> int:
        """
        方案号
        """
        pass

    @property
    def security_detail_id(self) -> str:
        """
        方案明细号
        """
        pass

    @property
    def operator_no(self) -> int:
        """
        操作员号
        """
        pass

    @property
    def is_nicked(self) -> bool:
        """
        是否匿名
        """
        pass

    @property
    def clear_speed(self) -> ClearSpeed:
        """
        清算速度
        """
        pass

    @property
    def counterparty_order_id(self) -> str:
        """
        对手方报价编号
        """
        pass

    @property
    def trade_type(self) -> TradeType:
        """
        交易所债券点价交易方式
        """
        pass
