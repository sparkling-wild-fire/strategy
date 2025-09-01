# -*- coding: utf-8 -*-
from datetime import datetime

from qt_strategy_base.core.model.base import BaseObject

from qt_strategy_base.model.enum import Side, Direction, CloseType, OrderStatus, InvestType


class CombOrderData(BaseObject):
    """
    合笔委托对象
    """

    @property
    def security(self) -> str:
        """
        代码
        """
        pass

    @property
    def id(self) -> int:
        """
        委托编号
        """
        pass

    @property
    def datetime(self) -> datetime:
        """
        委托时间
        """
        pass

    @property
    def status(self) -> OrderStatus:
        """
        委托状态
        """
        pass

    @property
    def buy_price(self) -> float:
        """
        买方向委托价格
        """
        pass

    @property
    def sell_price(self) -> float:
        """
        卖方向委托价格
        """
        pass

    @property
    def buy_quantity(self) -> float:
        """
        买方向委托数量
        """
        pass

    @property
    def sell_quantity(self) -> float:
        """
        卖方向委托数量
        """
        pass

    @property
    def buy_cancel_quantity(self) -> float:
        """
        买方向撤单数量
        """
        pass

    @property
    def sell_cancel_quantity(self) -> float:
        """
        卖方向撤单数量
        """
        pass

    @property
    def buy_direction(self) -> Direction:
        """
        买方向的开平方向
        """
        pass

    @property
    def sell_direction(self) -> Direction:
        """
        卖方向的开平方向
        """
        pass

    @property
    def buy_close_type(self) -> CloseType:
        """
        买方向的平仓类型
        """
        pass

    @property
    def sell_close_type(self) -> CloseType:
        """
        卖方向的平仓类型
        """
        pass


    @property
    def buy_id(self) -> int:
        """
        买方向委托序号(外部委托)
        """
        pass

    @property
    def sell_id(self) -> int:
        """
        卖方向委托序号(外部委托)
        """
        pass

    @property
    def buy_status(self) -> OrderStatus:
        """
        买方向委托状态
        """
        pass

    @property
    def sell_status(self) -> OrderStatus:
        """
        卖方向委托状态
        """
        pass

    @property
    def internal_id(self) -> str:
        """
        内部委托号
        """
        pass

    @property
    def invest_type(self) -> InvestType:
        """
        投资类型
        """
        pass

    @property
    def revoke_cause(self) -> str:
        """
        废单原因
        """
        pass

    @property
    def investunit_id(self) -> int:
        """
        账户 ID
        """
        pass

    @property
    def portfolio_id(self) -> int:
        """
        投资组合 ID
        """
        pass

    @property
    def buy_filled_quantity(self) -> float:
        """
        买方向成交数量
        """
        pass

    @property
    def sell_filled_quantity(self) -> float:
        """
        卖方向成交数量
        """
        pass

    @property
    def buy_filled_value(self) -> float:
        """
        买方向成交金额
        """
        pass

    @property
    def sell_filled_value(self) -> float:
        """
        卖方向成交金额
        """
        pass

    @property
    def remark(self) -> str:
        """
        备注消息
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
