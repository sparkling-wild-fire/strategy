# -- coding: utf-8 --
from abc import ABC
from typing import Tuple

from pandas import DataFrame

from qt_strategy_base.model.comb_order import CombOrderData
from qt_strategy_base.model.error_info import ErrorInfo
from qt_strategy_base.core.scheme.strategy_order_impl import OrderData
from qt_strategy_base.model.enum import Side, CloseType, Direction, ControlType, SecurityDetailStatus, ClearSpeed, \
    TradeType, SettleType, ClearType
from qt_strategy_base.model.strategy_api_data import AccountInfo
from qt_strategy_base.core.model.base import BaseObject


class SecurityDetail(BaseObject, ABC):

    @property
    def id(self) -> str:
        """
        证券明细号
        """
        pass

    @property
    def security(self) -> str:
        """
        证券明细代码
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
    def target_quantity(self) -> float:
        """
        目标数量
        """
        pass

    @property
    def control_type(self) -> ControlType:
        """
        控制类型
        """
        pass

    @property
    def total_volume(self) -> float:
        """
        累计成交数量
        """
        pass

    @property
    def total_value(self) -> float:
        """
        累计成交金额
        """
        pass

    @property
    def status(self) -> SecurityDetailStatus:
        """
        明细状态
        """
        pass

    @property
    def order_quantity(self) -> float:
        """
        累计委托数量
        """
        pass

    @property
    def order_value(self) -> float:
        """
        累计委托金额
        """
        pass

    def get_account(self) -> AccountInfo:
        """
        获取当前明细的账户
        @return:AccountInfo
        """
        pass

    def get_open_order_quantity_and_value(self, side: Side = None, direction: Direction = None) -> (float, float):
        """
        获取挂单量和挂单金额
        @param side: 委托方向
        @param direction: 开平方向
        @return:
        """
        pass

    def get_volume_and_value(self, side: Side = None, direction: Direction = None) -> (float, float):
        """
        获取成交量和成交金额
        @param side: 委托方向
        @param direction: 开平方向
        @return:
        """
        pass

    def get_orders(self) -> DataFrame:
        """
        获取明细下的委托
        @return:DataFrame
        """
        pass

    def order(self, price: float, quantity: float, side: Side = None, direction: Direction = None,
              close_type: CloseType = None, remark: str = "") -> Tuple[ErrorInfo, OrderData]:
        """
       单笔委托（匹配成交）
        @param price: 委托价格
        @param quantity: 委托数量
        @param side: 委托方向
        @param direction: 开平方向
        @param close_type: 平仓类型
        @param remark: 委托备注
        @return:错误信息，委托的元组
        """
        pass

    def click_order(self, price: float, quantity: float, side: Side = None, clear_speed: ClearSpeed = None,
                    is_nicked: bool = True, counterparty_order_id: str = "", trade_type: TradeType = TradeType.DEFAULT,
                    remark: str = "") -> Tuple[ErrorInfo, OrderData]:
        """
        单笔委托（点击成交）
        @param price:委托价格
        @param quantity:委托数量
        @param side:委托方向
        @param clear_speed:清算速度，不区分:-1 ,0:T+0 ,1:T+1
        @param is_nicked:是否匿名
        @param counterparty_order_id:上交所传入买入/卖出报价ID，深交所传入报价消息编号
        @param trade_type:交易所债券点价交易类型 1-全额成交 0 -默认
        @param remark:委托备注
        @return:错误信息，委托的元组
        """
        pass

    def comb_order(self, buy_quantity: float, sell_quantity: float, buy_price: float, sell_price: float,
                   buy_direction: Direction = None, sell_direction: Direction = None, buy_close_type: CloseType = None,
                   sell_close_type: CloseType = None, clear_speed: ClearSpeed = None,
                   replace_order_id: str = "", remark: str = "", is_nicked=True) -> Tuple[ErrorInfo, CombOrderData]:
        """
        合笔委托（匹配成交）
        @param buy_quantity:买委托数量
        @param sell_quantity:卖委托数量
        @param buy_price:买委托价格
        @param sell_price:卖委托价格
        @param buy_direction:买委托开平方向
        @param sell_direction:卖委托开平方向
        @param buy_close_type:买委托平仓类型
        @param sell_close_type:卖委托平仓类型
        @param clear_speed:清算速度
        @param replace_order_id:顶单号
        @param remark:备注
        @param is_nicked:是否匿名
        @return:错误信息，委托的元组
        """
        pass

    def intrabank_comb_order(self, buy_quantity: float, sell_quantity: float, buy_price: float, sell_price: float,
                             expire_time: int, iceberg_quantity: float, settle_type: SettleType, clear_type: ClearType,
                             remark: str = "", is_nicked=True) -> Tuple[ErrorInfo, CombOrderData]:
        """
        合笔委托（银行间债券做市）
        @param buy_quantity: 买委托数量
        @param sell_quantity: 卖委托数量
        @param buy_price: 买委托价格
        @param sell_price: 卖委托价格
        @param expire_time: 委托到期时间-银行间 HHMMSS
        @param iceberg_quantity: 冰山券面-银行间
        @param settle_type: 结算方式-买卖同一个值-银行间
        @param clear_type: 清算速度-银行间必传
        @param remark: 备注
        @param is_nicked: 是否匿名
        @return: 
        """
        pass
