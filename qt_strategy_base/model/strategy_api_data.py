# -*- coding: UTF-8 -*
import datetime
import time
from abc import ABC

from qt_strategy_base.core.common import python_logger
from qt_strategy_base.core.common.public_func import covert_to_enum, int_time_to_str
from qt_strategy_base.core.model.base import BaseObject
from qt_strategy_base.core.model.model import PQDBJHqInfo, PCJHqInfo, PXBondOrder, PXBondBaseInfo, \
    PYHJBondMMInfo, PYHJBondMMOrder
from qt_strategy_base.model.enum import *
import  base64

class SnapshotData(BaseObject, ABC):
    """
    快照
    """

    def __init__(self, data_info):
        from qt_strategy_base.core.model.model import PSnapshotData
        self._data_info: PSnapshotData = data_info

    @property
    def security(self) -> str:
        """
        代码
        """
        return self._data_info.security

    @property
    def high(self) -> float:
        """
        最高价
        """
        return self._data_info.high

    @property
    def open(self) -> float:
        """
        开盘价
        """
        return self._data_info.open

    @property
    def low(self) -> float:
        """
        最低价
        """
        return self._data_info.low

    @property
    def last(self) -> float:
        """
        最新价
        """
        return self._data_info.last

    @property
    def limit_up(self) -> float:
        """
        涨停价
        """
        return self._data_info.limit_up

    @property
    def limit_down(self) -> float:
        """
        跌停价
        """
        return self._data_info.limit_down

    @property
    def volume(self) -> float:
        """
        交易量
        """
        return self._data_info.volume

    @property
    def value(self) -> float:
        """
        交易金额
        """
        return self._data_info.value

    @property
    def pre_close(self) -> float:
        """
        昨收价
        """
        return self._data_info.pre_close

    @property
    def settlement(self) -> float:
        """
        结算价
        """
        return self._data_info.settlement

    @property
    def open_interest(self) -> float:
        """
        持仓量
        """
        return self._data_info.open_interest

    @property
    def pre_settlement(self) -> float:
        """
        昨结价
        """
        return self._data_info.pre_settlement

    @property
    def status(self) -> SnapshotStatus:
        """
        行情状态
        """
        return covert_to_enum(self._data_info.status, SnapshotStatus)

    @property
    def time(self) -> str:
        """
        时间戳
        """
        return int_time_to_str(self._data_info.time)

    @property
    def iopv(self) -> float:
        """
        基金净值
        """
        return self._data_info.iopv

    @property
    def bid(self) -> dict:
        """
        买档
        """
        return self._data_info.bid

    @property
    def ask(self) -> dict:
        """
        卖档
        """
        return self._data_info.ask


class NeeqSnapshotData(BaseObject, ABC):
    """
    股转投资者和做市商行情
    """

    def __init__(self, data_info):
        from qt_strategy_base.core.model.model import PNeeqSnapshotData
        self._data_info: PNeeqSnapshotData = data_info

    @property
    def security(self) -> str:
        """
        代码
        """
        return self._data_info.security

    @property
    def maker_time(self) -> str:
        """
        做市商行情时间
        """
        return int_time_to_str(self._data_info.maker_time)

    @property
    def investor_time(self) -> str:
        """
        投资者行情时间
        """
        return int_time_to_str(self._data_info.investor_time)

    @property
    def maker_bid(self) -> list:
        """
        做市商买档
        """
        return self._data_info.maker_bid

    @property
    def maker_ask(self) -> list:
        """
        做市商卖档
        """
        return self._data_info.maker_ask

    @property
    def investor_bid(self) -> list:
        """
        投资者买档
        """
        return self._data_info.investor_bid

    @property
    def investor_ask(self) -> list:
        """
        投资者卖档
        """
        return self._data_info.investor_ask


class BarData(BaseObject, ABC):
    """
    分钟对象
    """

    def __init__(self, data_info):
        from qt_strategy_base.core.model.model import PBarData
        self._data_info: PBarData = data_info

    @property
    def security(self) -> str:
        """
        代码
        """
        return self._data_info.security

    @property
    def date(self) -> str:
        """
        日期
        """
        return self._data_info.date

    @property
    def time(self) -> str:
        """
        时间
        """
        return self._data_info.time

    @property
    def open(self) -> float:
        """
        开盘价
        """
        return self._data_info.open

    @property
    def low(self) -> float:
        """
        最低价
        """
        return self._data_info.low

    @property
    def high(self) -> float:
        """
        最新价
        """
        return self._data_info.high

    @property
    def close(self) -> float:
        """
        收盘价
        """
        return self._data_info.close

    @property
    def pre_close(self) -> float:
        """
        昨收价
        """
        return self._data_info.pre_close

    @property
    def volume(self) -> float:
        """
        成交量
        """
        return self._data_info.volume

    @property
    def value(self) -> float:
        """
        成交额
        """
        return self._data_info.value


class TradeData(BaseObject, ABC):
    """
    成交对象
    """

    def __init__(self, data_info):
        from qt_strategy_base.core.model.model import PTradeData
        self._data_info: PTradeData = data_info

    @property
    def security(self) -> str:
        """
        代码
        """
        return self._data_info.security

    @property
    def id(self) -> int:
        """
        成交编号
        """
        return self._data_info.id

    @property
    def datetime(self) -> str:
        """
        成交时间
        """
        if self._data_info.datetime is None:
            return None
        else:
            return datetime.datetime.fromtimestamp(self._data_info.datetime)

    @property
    def volume(self) -> float:
        """
        成交数量
        """
        return self._data_info.volume

    @property
    def value(self) -> float:
        """
        成交金额
        """
        return self._data_info.value

    @property
    def order_quantity(self) -> float:
        """
        委托数量
        """
        return self._data_info.order_quantity

    @property
    def side(self) -> Side:
        """
        委托方向
        """
        return covert_to_enum(self._data_info.side, Side)

    @property
    def direction(self) -> Direction:
        """
        开平方向
        """
        return covert_to_enum(self._data_info.direction, Direction)

    @property
    def close_type(self) -> CloseType:
        """
        平仓方向
        """
        return covert_to_enum(self._data_info.close_type, CloseType)

    @property
    def internal_id(self) -> str:
        """
        内部委托号
        """
        return self._data_info.internal_id

    @property
    def order_id(self) -> int:
        """
        外部委托编号
        """
        return self._data_info.order_id

    @property
    def invest_type(self) -> InvestType:
        """
        投资类型
        """
        return covert_to_enum(self._data_info.invest_type, InvestType)

    @property
    def fee(self) -> float:
        """
        当次费用
        """
        return self._data_info.fee

    @property
    def total_volume(self) -> float:
        """
        累计成交数量
        """
        return self._data_info.total_volume

    @property
    def total_value(self) -> float:
        """
        累计成交金额
        """
        return self._data_info.total_value

    @property
    def remark(self) -> str:
        """
        备注
        """
        return self._data_info.remark

    @property
    def investunit_id(self) -> int:
        """
        账户 ID
        """
        return self._data_info.investunit_id

    @property
    def portfolio_id(self) -> int:
        """
        投资组合 ID
        """
        return self._data_info.portfolio_id

    @property
    def scheme_id(self) -> int:
        """
        方案号
        """
        return self._data_info.scheme_id

    @property
    def security_detail_id(self) -> str:
        """
        方案明细号
        """
        return self._data_info.security_detail_id


class PositionData(BaseObject, ABC):
    """
    持仓对象
    """

    def __init__(self, data_info):
        from qt_strategy_base.core.model.model import PPositionData
        self._data_info: PPositionData = data_info

    @property
    def security(self) -> str:
        """
        代码
        """
        return self._data_info.security

    @property
    def invest_type(self) -> InvestType:
        """
        投资类型
        """
        return covert_to_enum(self._data_info.invest_type, InvestType)

    @property
    def position_type(self) -> PositionType:
        """
        多空类型
        """
        return covert_to_enum(self._data_info.position_type, PositionType)

    @property
    def initial_position(self) -> float:
        """
        期初数量
        """
        return self._data_info.initial_position

    @property
    def position(self) -> float:
        """
        当前持仓数量
        """
        return self._data_info.position

    @property
    def available_position(self) -> float:
        """
        可用数量
        """
        return self._data_info.available_position

    @property
    def yesterday_available_position(self) -> float:
        """
        昨仓可用数量
        """
        return self._data_info.yesterday_available_position

    @property
    def today_available_position(self) -> float:
        """
        今仓可用
        """
        return self._data_info.today_available_position

    @property
    def buy_volume(self) -> float:
        """
        当日买成交数量
        """
        return self._data_info.buy_volume

    @property
    def buy_value(self) -> float:
        """
        当日买成交金额
        """
        return self._data_info.buy_value

    @property
    def sell_volume(self) -> float:
        """
        当日卖成交数量
        """
        return self._data_info.sell_volume

    @property
    def sell_value(self) -> float:
        """
        当日卖成交金额
        """
        return self._data_info.sell_value

    @property
    def unfilled_order_buy_quantity(self) -> float:
        """
        买挂单数量
        """
        return self._data_info.unfilled_order_buy_quantity

    @property
    def unfilled_order_sell_quantity(self) -> float:
        """
        卖挂单数量
        """
        return self._data_info.unfilled_order_sell_quantity

    @property
    def frozen_quantity(self) -> float:
        """
        冻结数量
        """
        return self._data_info.frozen_quantity

    @property
    def cost(self) -> float:
        """
        持仓成本
        """
        return self._data_info.cost

    @property
    def total_fee(self) -> float:
        """
        持仓费用
        """
        return self._data_info.total_fee

    @property
    def investunit_id(self) -> int:
        """
        账户 ID
        """
        return self._data_info.investunit_id

    @property
    def portfolio_id(self) -> int:
        """
        投资组合 ID
        """
        return self._data_info.portfolio_id
    
    @property
    def etf_purchase_quantity(self) -> float:
        """
        etf申购成交数量
        """
        return self._data_info.etf_purchase_quantity    
    
    @property
    def etf_redeem_quantity(self) -> float:
        """
        etf赎回成交数量
        """
        return self._data_info.etf_redeem_quantity
        


class MarketDutyData(BaseObject, ABC):
    """
    做市义务对象
    """

    def __init__(self, data_info):
        from qt_strategy_base.core.model.model import PMarketDutyData
        self._data_info: PMarketDutyData = data_info

    @property
    def security(self) -> str:
        """
        代码
        """
        return self._data_info.security

    @property
    def optimal_buy_value(self) -> float:
        """
        最优买金额
        """
        return self._data_info.optimal_buy_value

    @property
    def optimal_sell_value(self) -> float:
        """
        最优卖金额
        """
        return self._data_info.optimal_sell_value

    @property
    def optimal_buy_quantity(self) -> float:
        """
        最优买量
        """
        return self._data_info.optimal_buy_quantity

    @property
    def optimal_sell_quantity(self) -> float:
        """
        最优卖量
        """
        return self._data_info.optimal_sell_quantity

    @property
    def max_buy_price(self) -> float:
        """
        最高买入价
        """
        return self._data_info.max_buy_price

    @property
    def min_sell_price(self) -> float:
        """
        最低卖出价
        """
        return self._data_info.min_sell_price

    @property
    def min_spread_rate(self) -> float:
        """
        最小报价差比
        """
        return self._data_info.min_spread_rate

    @property
    def optimal_spread(self) -> float:
        """
        最优价差
        """
        return self._data_info.optimal_spread

    @property
    def buy_volume(self) -> float:
        """
        买成交数量
        """
        return self._data_info.buy_volume

    @property
    def sell_volume(self) -> float:
        """
        卖成交数量
        """
        return self._data_info.sell_volume

    @property
    def open_auction_quote_flag(self) -> str:
        """
        开盘集合竞价时段报价标识
        """
        return self._data_info.open_auction_quote_flag

    @property
    def avg_declared_value(self) -> float:
        """
        平均每笔申报金额
        """
        return self._data_info.avg_declared_value

    @property
    def exempt_duration(self) -> int:
        """
        做市豁免时长
        """
        return self._data_info.exempt_duration

    @property
    def suspended_duration(self) -> int:
        """
        停牌时长
        """
        return self._data_info.suspended_duration

    @property
    def exempt_status(self) -> str:
        """
        豁免状态
        """
        return self._data_info.exempt_status

    @property
    def current_invalid_duration(self) -> int:
        """
        当前无效时长
        """
        return self._data_info.current_invalid_duration

    @property
    def today_invalid_duration(self) -> int:
        """
        当日无效时长
        """
        return self._data_info.today_invalid_duration

    @property
    def current_market_time_rate(self) -> float:
        """
        当前做市时间比例
        """
        return self._data_info.current_market_time_rate

    @property
    def today_market_time_rate(self) -> float:
        """
        当日做市时间比例
        """
        return self._data_info.today_market_time_rate

    @property
    def is_satisfy_market_duty(self) -> str:
        """
        是否满足做市义务
        """
        return self._data_info.is_satisfy_market_duty

    @property
    def TWAP_spread(self) -> float:
        """
        时间加权平均买卖价差
        """
        return self._data_info.TWAP_spread

    @property
    def buy_quantity(self) -> float:
        """
        买方向委托数量
        """
        return self._data_info.buy_quantity

    @property
    def sell_quantity(self) -> float:
        """
        卖方向委托数量
        """
        return self._data_info.sell_quantity

    @property
    def adjust_time(self) -> int:
        """
        调整时间
        """
        return self._data_info.adjust_time

    @property
    def business_classification(self) -> str:
        """
        业务分类
        """
        return self._data_info.business_classification

    @property
    def TWAP_spread_rate(self) -> float:
        """
        时间加权平均买卖价差率
        """
        return self._data_info.TWAP_spread_rate

    @property
    def total_spread_rate(self) -> float:
        """
        累计买卖价差比
        """
        return self._data_info.total_spread_rate

    @property
    def close_participation_rate(self) -> float:
        """
        收盘集合竞价参与率
        """
        return self._data_info.close_participation_rate

    @property
    def open_participation_rate(self) -> float:
        """
        开盘集合竞价参与率
        """
        return self._data_info.open_participation_rate

    @property
    def trading_curb_participation_rate(self) -> float:
        """
        熔断集合竞价参与率
        """
        return self._data_info.trading_curb_participation_rate


class SecurityBaseInfo(BaseObject, ABC):
    """
    证券基础信息
    """

    def __init__(self, data_info):
        from qt_strategy_base.core.model.model import PSecurityBaseInfo
        self._data_info: PSecurityBaseInfo = data_info

    @property
    def security(self) -> str:
        """
        代码
        """
        return self._data_info.security

    @property
    def security_type(self) -> SecurityType:
        """
        证券类型
        """
        return covert_to_enum(self._data_info.security_type, SecurityType)

    @property
    def buy_unit(self) -> int:
        """
        买单位
        """
        return self._data_info.buy_unit

    @property
    def sell_unit(self) -> int:
        """
        卖单位
        """
        return self._data_info.sell_unit

    @property
    def buy_qty_max(self) -> float:
        """
        最大买入数量
        """
        return self._data_info.buy_qty_max

    @property
    def sell_qty_max(self) -> float:
        """
        最大卖出数量
        """
        return self._data_info.sell_qty_max

    @property
    def market_buy_qty_max(self) -> float:
        """
        最大市价买入数量
        """
        return self._data_info.market_buy_qty_max

    @property
    def market_sell_qty_max(self) -> float:
        """
        最大市价卖出数量
        """
        return self._data_info.market_sell_qty_max

    @property
    def contract_multiplier(self) -> int:
        """
        合约乘数
        """
        return self._data_info.contract_multiplier

    @property
    def minimal_price_spread(self) -> float:
        """
        最小买卖价差
        """
        return self._data_info.minimal_price_spread

    @property
    def buy_qty_min(self) -> float:
        """
        最小买入数量
        """
        return self._data_info.buy_qty_min

    @property
    def sell_qty_min(self) -> float:
        """
        最小卖出数量
        """
        return self._data_info.sell_qty_min

    @property
    def board_type(self) -> BoardType:
        """
        板块
        """
        return covert_to_enum(self._data_info.board_type, BoardType)

    @property
    def total_shares(self) -> float:
        """
        总股本
        """
        return self._data_info.total_shares

    @property
    def outstanding_shares(self) -> float:
        """
        流通股本
        """
        return self._data_info.outstanding_shares


class StockBaseInfo(BaseObject, ABC):
    """
    股票基础信息
    """

    def __init__(self, data_info):
        from qt_strategy_base.core.model.model import PStockBaseInfo
        self._data_info: PStockBaseInfo = data_info

    @property
    def security(self) -> str:
        """
        代码
        """
        return self._data_info.security

    @property
    def security_type(self) -> SecurityType:
        """
        证券类型
        """
        return covert_to_enum(self._data_info.security_type, SecurityType)

    @property
    def buy_unit(self) -> int:
        """
        买单位
        """
        return self._data_info.buy_unit

    @property
    def sell_unit(self) -> int:
        """
        卖单位
        """
        return self._data_info.sell_unit

    @property
    def buy_qty_max(self) -> float:
        """
        最大买入数量
        """
        return self._data_info.buy_qty_max

    @property
    def sell_qty_max(self) -> float:
        """
        最大卖出数量
        """
        return self._data_info.sell_qty_max

    @property
    def market_buy_qty_max(self) -> float:
        """
        最大市价买入数量
        """
        return self._data_info.market_buy_qty_max

    @property
    def market_sell_qty_max(self) -> float:
        """
        最大市价卖出数量
        """
        return self._data_info.market_sell_qty_max

    @property
    def contract_multiplier(self) -> int:
        """
        合约乘数
        """
        return self._data_info.contract_multiplier

    @property
    def minimal_price_spread(self) -> float:
        """
        最小买卖价差
        """
        return self._data_info.minimal_price_spread

    @property
    def buy_qty_min(self) -> float:
        """
        最小买入数量
        """
        return self._data_info.buy_qty_min

    @property
    def sell_qty_min(self) -> float:
        """
        最小卖出数量
        """
        return self._data_info.sell_qty_min

    @property
    def board_type(self) -> BoardType:
        """
        板块
        """
        return covert_to_enum(self._data_info.board_type, BoardType)

    @property
    def total_shares(self) -> float:
        """
        总股本
        """
        return self._data_info.total_shares

    @property
    def outstanding_shares(self) -> float:
        """
        流通股本
        """
        return self._data_info.outstanding_shares


class BondBaseInfo(BaseObject, ABC):
    """
    债券基础信息
    """

    def __init__(self, data_info):
        from qt_strategy_base.core.model.model import PBondBaseInfo
        self._data_info: PBondBaseInfo = data_info

    @property
    def security(self) -> str:
        """
        代码
        """
        return self._data_info.security

    @property
    def security_type(self) -> SecurityType:
        """
        证券类型
        """
        return covert_to_enum(self._data_info.security_type, SecurityType)

    @property
    def buy_unit(self) -> int:
        """
        买单位
        """
        return self._data_info.buy_unit

    @property
    def sell_unit(self) -> int:
        """
        卖单位
        """
        return self._data_info.sell_unit

    @property
    def buy_qty_max(self) -> float:
        """
        最大买入数量
        """
        return self._data_info.buy_qty_max

    @property
    def sell_qty_max(self) -> float:
        """
        最大卖出数量
        """
        return self._data_info.sell_qty_max

    @property
    def market_buy_qty_max(self) -> float:
        """
        最大市价买入数量
        """
        return self._data_info.market_buy_qty_max

    @property
    def market_sell_qty_max(self) -> float:
        """
        最大市价卖出数量
        """
        return self._data_info.market_sell_qty_max

    @property
    def contract_multiplier(self) -> int:
        """
        合约乘数
        """
        return self._data_info.contract_multiplier

    @property
    def minimal_price_spread(self) -> float:
        """
        最小买卖价差
        """
        return self._data_info.minimal_price_spread

    @property
    def buy_qty_min(self) -> float:
        """
        最小买入数量
        """
        return self._data_info.buy_qty_min

    @property
    def sell_qty_min(self) -> float:
        """
        最小卖出数量
        """
        return self._data_info.sell_qty_min

    @property
    def board_type(self) -> BoardType:
        """
        板块
        """
        return covert_to_enum(self._data_info.board_type, BoardType)

    @property
    def total_shares(self) -> float:
        """
        总股本
        """
        return self._data_info.total_shares

    @property
    def outstanding_shares(self) -> float:
        """
        流通股本
        """
        return self._data_info.outstanding_shares

    @property
    def face_value(self) -> float:
        """
        面值
        """
        return self._data_info.face_value

    @property
    def interests(self) -> float:
        """
        百元债券利息
        """
        return self._data_info.interests

    @property
    def change_price(self) -> float:
        """
        转股价
        """
        return self._data_info.change_price

    @property
    def remaining_term(self) -> float:
        """
        剩余期限（年）
        """
        return self._data_info.remaining_term


class FuturesBaseInfo(BaseObject, ABC):
    """
    期货基础信息
    """

    def __init__(self, data_info):
        from qt_strategy_base.core.model.model import PFuturesBaseInfo
        self._data_info: PFuturesBaseInfo = data_info

    @property
    def security(self) -> str:
        """
        代码
        """
        return self._data_info.security

    @property
    def security_type(self) -> SecurityType:
        """
        证券类型
        """
        return covert_to_enum(self._data_info.security_type, SecurityType)

    @property
    def buy_unit(self) -> int:
        """
        买单位
        """
        return self._data_info.buy_unit

    @property
    def sell_unit(self) -> int:
        """
        卖单位
        """
        return self._data_info.sell_unit

    @property
    def buy_qty_max(self) -> float:
        """
        最大买入数量
        """
        return self._data_info.buy_qty_max

    @property
    def sell_qty_max(self) -> float:
        """
        最大卖出数量
        """
        return self._data_info.sell_qty_max

    @property
    def market_buy_qty_max(self) -> float:
        """
        最大市价买入数量
        """
        return self._data_info.market_buy_qty_max

    @property
    def market_sell_qty_max(self) -> float:
        """
        最大市价卖出数量
        """
        return self._data_info.market_sell_qty_max

    @property
    def contract_multiplier(self) -> int:
        """
        合约乘数
        """
        return self._data_info.contract_multiplier

    @property
    def minimal_price_spread(self) -> float:
        """
        最小买卖价差
        """
        return self._data_info.minimal_price_spread

    @property
    def buy_qty_min(self) -> float:
        """
        最小买入数量
        """
        return self._data_info.buy_qty_min

    @property
    def sell_qty_min(self) -> float:
        """
        最小卖出数量
        """
        return self._data_info.sell_qty_min

    @property
    def board_type(self) -> BoardType:
        """
        板块
        """
        return covert_to_enum(self._data_info.board_type, BoardType)

    @property
    def total_shares(self) -> float:
        """
        总股本
        """
        return self._data_info.total_shares

    @property
    def outstanding_shares(self) -> float:
        """
        流通股本
        """
        return self._data_info.outstanding_shares

    @property
    def last_trade_date(self) -> int:
        """
        最后交易日期
        """
        return self._data_info.last_trade_date

    @property
    def last_trade_time(self) -> int:
        """
        最后交易时间
        """
        return self._data_info.last_trade_time

    @property
    def settlement_month(self) -> int:
        """
        交割年月
        """
        return self._data_info.settlement_month

    @property
    def settlement_date(self) -> int:
        """
        交割日期
        """
        return self._data_info.settlement_date


class OptionBaseInfo(BaseObject, ABC):
    """
    期权基础信息
    """

    def __init__(self, data_info):
        from qt_strategy_base.core.model.model import POptionBaseInfo
        self._data_info: POptionBaseInfo = data_info

    @property
    def security(self) -> str:
        """
        代码
        """
        return self._data_info.security

    @property
    def security_type(self) -> SecurityType:
        """
        证券类型
        """
        return covert_to_enum(self._data_info.security_type, SecurityType)

    @property
    def buy_unit(self) -> int:
        """
        买单位
        """
        return self._data_info.buy_unit

    @property
    def sell_unit(self) -> int:
        """
        卖单位
        """
        return self._data_info.sell_unit

    @property
    def buy_qty_max(self) -> float:
        """
        最大买入数量
        """
        return self._data_info.buy_qty_max

    @property
    def sell_qty_max(self) -> float:
        """
        最大卖出数量
        """
        return self._data_info.sell_qty_max

    @property
    def market_buy_qty_max(self) -> float:
        """
        最大市价买入数量
        """
        return self._data_info.market_buy_qty_max

    @property
    def market_sell_qty_max(self) -> float:
        """
        最大市价卖出数量
        """
        return self._data_info.market_sell_qty_max

    @property
    def contract_multiplier(self) -> int:
        """
        合约乘数
        """
        return self._data_info.contract_multiplier

    @property
    def minimal_price_spread(self) -> float:
        """
        最小买卖价差
        """
        return self._data_info.minimal_price_spread

    @property
    def buy_qty_min(self) -> float:
        """
        最小买入数量
        """
        return self._data_info.buy_qty_min

    @property
    def sell_qty_min(self) -> float:
        """
        最小卖出数量
        """
        return self._data_info.sell_qty_min

    @property
    def board_type(self) -> BoardType:
        """
        板块
        """
        return covert_to_enum(self._data_info.board_type, BoardType)

    @property
    def total_shares(self) -> float:
        """
        总股本
        """
        return self._data_info.total_shares

    @property
    def outstanding_shares(self) -> float:
        """
        流通股本
        """
        return self._data_info.outstanding_shares

    @property
    def underlying(self) -> str:
        """
        标的代码
        """
        return self._data_info.underlying

    @property
    def type(self) -> OptionType:
        """
        期权类型
        """
        return covert_to_enum(self._data_info.type, OptionType)

    @property
    def exercise_type(self) -> OptionExerciseType:
        """
        行权类型
        """
        return covert_to_enum(self._data_info.exercise_type, OptionExerciseType)

    @property
    def strike_price(self) -> float:
        """
        行权价
        """
        return self._data_info.strike_price

    @property
    def begin_trade_date(self) -> int:
        """
        开始交易日期
        """
        return self._data_info.begin_trade_date

    @property
    def end_trade_date(self) -> int:
        """
        结束交易日期
        """
        return self._data_info.end_trade_date

    @property
    def exercise_begin_date(self) -> int:
        """
        行权起始日期
        """
        return self._data_info.exercise_begin_date

    @property
    def exercise_end_date(self) -> int:
        """
        行权结束日期
        """
        return self._data_info.exercise_end_date

    @property
    def exercise_month(self) -> int:
        """
        到期月份
        """
        return self._data_info.exercise_month


class ETFInfo(BaseObject, ABC):
    """
    ETF信息
    """

    def __init__(self, data_info):
        from qt_strategy_base.core.model.model import PETFInfo
        self._data_info: PETFInfo = data_info

    @property
    def security(self) -> str:
        """
        代码
        """
        return self._data_info.security

    @property
    def stock_num(self) -> float:
        """
        获取成分股数量
        """
        return self._data_info.stock_num

    @property
    def minimal_subscribe_unit(self) -> int:
        """
        获取ETF申报单位
        """
        return self._data_info.minimal_subscribe_unit

    @property
    def max_cash_rep_ratio(self) -> float:
        """
        获取现金比例上限
        """
        return self._data_info.max_cash_rep_ratio

    @property
    def publish_type(self) -> ETFPublishType:
        """
        信息发布标志
        """
        return covert_to_enum(self._data_info.publish_type, ETFPublishType)

    @property
    def status(self) -> ETFStatus:
        """
        当天状态
        """
        return covert_to_enum(self._data_info.status, ETFStatus)

    @property
    def estimated_cash_balance(self) -> float:
        """
        t日预估现金余额
        """
        return self._data_info.estimated_cash_balance

    @property
    def market_type(self) -> ETFMarketType:
        """
        ETF类型
        """
        return covert_to_enum(self._data_info.market_type, ETFMarketType)

    @property
    def constituent_type(self) -> ETFConstituentType:
        """
        ETF成分股类型
        """
        return covert_to_enum(self._data_info.constituent_type, ETFConstituentType)

    @property
    def sub_red_type(self) -> SubNRedType:
        """
        ETF申赎类型
        """
        return covert_to_enum(self._data_info.sub_red_type, SubNRedType)

    @property
    def pre_nav(self) -> float:
        """
        获取基金份额净值
        """
        return self._data_info.pre_nav

    @property
    def pre_unit_nav(self)->float:
        """
        获取基金单位净值
        """
        return self._data_info.pre_unit_nav

class ETFConstituent(BaseObject, ABC):
    """
    ETF成分股
    """

    def __init__(self, data_info):
        from qt_strategy_base.core.model.model import PETFConstituent
        self._data_info: PETFConstituent = data_info

    @property
    def security(self) -> str:
        """
        证券代码
        """
        return self._data_info.security

    @property
    def quantity(self) -> float:
        """
        数量
        """
        return self._data_info.quantity

    @property
    def cash_rep_type(self) -> ETFCashReplaceType:
        """
        现金替代标志
        """
        return covert_to_enum(self._data_info.cash_rep_type, ETFCashReplaceType)

    @property
    def subscribe_rep_premium_ratio(self) -> float:
        """
        申购现金替代溢价比率
        """
        return self._data_info.subscribe_rep_premium_ratio

    @property
    def redeem_rep_discount_ratio(self) -> float:
        """
        赎回现金替代折价比率
        """
        return self._data_info.redeem_rep_discount_ratio

    @property
    def subscribe_rep_value(self) -> float:
        """
        申购替代金额
        """
        return self._data_info.subscribe_rep_value

    @property
    def redeem_rep_value(self) -> float:
        """
        赎回替代金额
        """
        return self._data_info.redeem_rep_value


class AccountFund(BaseObject, ABC):
    """
    账户资金
    """

    def __init__(self, data_info):
        from qt_strategy_base.core.model.model import PAccountFund
        self._data_info: PAccountFund = data_info

    @property
    def T0_balance(self) -> float:
        """
        T+0 可用
        """
        return self._data_info.T0_balance

    @property
    def T1_balance(self) -> float:
        """
        T+1 可用
        """
        return self._data_info.T1_balance

    @property
    def margin_available(self) -> float:
        """
        保证金可用
        """
        return self._data_info.margin_available

    @property
    def margin_occupy(self) -> float:
        """
        保证金占用
        """
        return self._data_info.margin_occupy

    @property
    def margin_balance(self) -> float:
        """
        保证金账户余额
        """
        return self._data_info.margin_balance

    @property
    def margin_unfilled_order_occupy(self) -> float:
        """
        挂单占用保证金
        """
        return self._data_info.margin_unfilled_order_occupy


class AccountInfo(BaseObject, ABC):
    """
    账户信息
    """

    def __init__(self, investunit_id, invest_type, portfolio_id):
        self._investunit_id: int = investunit_id
        self._invest_type: str = invest_type
        self._portfolio_id: int = portfolio_id

    @property
    def investunit_id(self) -> int:
        """
        投资单元id
        """
        return self._investunit_id

    @property
    def portfolio_id(self) -> int:
        """
        投资组合id
        """
        return self._portfolio_id

    @property
    def invest_type(self) -> InvestType:
        """
        投资类型
        """
        return covert_to_enum(self._invest_type, InvestType)


class Factor(BaseObject, ABC):
    """
    标准因子
    """

    def __init__(self, data_info):
        from qt_strategy_base.core.model.model import PFactor
        self._data_info: PFactor = data_info

    @property
    def security(self) -> str:
        """
        证券代码
        """
        return self._data_info.security

    @property
    def factor_name(self) -> str:
        """
        因子名称
        """
        return self._data_info.factor_name

    @property
    def factor_value(self) -> float:
        """
        投资类型
        """
        return self._data_info.factor_value

    @property
    def update_time(self) -> datetime:
        """
        更新时间
        """
        update_time = None
        try:
            update_time = datetime.datetime.fromtimestamp(self._data_info.time_stamp, tz=None)
        except Exception as e:
            python_logger.error(f"{self._data_info.time_stamp}转换成datatime失败！原因:{e}")
        return update_time


class BondQDBJInfo(BaseObject, ABC):
    def __init__(self, qdbj_data_info):
        self._qdbj_data_info: PQDBJHqInfo = qdbj_data_info

    @property
    def security(self) -> str:
        """
        代码
        """
        return self._qdbj_data_info.security

    @property
    def level_no(self) -> int:
        """
        档位序号
        """
        return self._qdbj_data_info.level_no

    @property
    def order_id(self) -> str:
        """
        订单编号
        """
        return self._qdbj_data_info.order_id

    @property
    def quote_time(self) -> int:
        """
        卖档
        """
        return self._qdbj_data_info.quote_time

    @property
    def net_price(self) -> float:
        """
        卖档
        """
        return self._qdbj_data_info.net_price

    @property
    def quantity(self) -> float:
        """
        卖档
        """
        return self._qdbj_data_info.quantity

    @property
    def quoter(self) -> str:
        """
        卖档
        """
        return self._qdbj_data_info.quoter

    @property
    def clear_speed(self) -> ClearSpeed:
        """
        卖档
        """
        return covert_to_enum(self._qdbj_data_info.clear_speed, ClearSpeed)


class BondClickHq(BaseObject, ABC):

    def __init__(self, qdbj_data_info, cj_data_info):
        if qdbj_data_info is not None:
            self._qdbj_data_info: dict = qdbj_data_info
        else:
            self._qdbj_data_info: dict = {"buy_info": [], "sale_info": []}
        if cj_data_info is not None:
            self._cj_data_info: PCJHqInfo = cj_data_info
        else:
            self._cj_data_info: PCJHqInfo = PCJHqInfo("", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    @property
    def security(self) -> str:
        """
        代码
        """
        return self._cj_data_info.security

    @property
    def datetime(self) -> datetime:
        """
        成交时间
        @return:
        """

        if self._cj_data_info.datetime is None:
            return None
        else:
            return datetime.datetime.fromtimestamp(self._cj_data_info.datetime)

    @property
    def open(self) -> float:
        """
        开盘价
        """
        return self._cj_data_info.open

    @property
    def high(self) -> float:
        """
        最高价
        """
        return self._cj_data_info.high

    @property
    def low(self) -> float:
        """
        最低价
        """
        return self._cj_data_info.low

    @property
    def last(self) -> float:
        """
        最新价
        """
        return self._cj_data_info.last

    @property
    def wwap(self) -> float:
        """
        当日加权平均价
        """
        return self._cj_data_info.wwap

    @property
    def pre_close(self) -> float:
        """
        昨收盘价
        """
        return self._cj_data_info.pre_close

    @property
    def pre_vwap(self) -> float:
        """
        昨日加权平均价
        """
        return self._cj_data_info.pre_vwap

    @property
    def volume(self) -> float:
        """
        成交数量
        """
        return self._cj_data_info.volume

    @property
    def total_volume(self) -> float:
        """
        当日总成交量（手）
        """
        return self._cj_data_info.total_volume

    @property
    def total_value(self) -> float:
        """
       当日总成交金额
        """
        return self._cj_data_info.total_value

    @property
    def total_num(self) -> float:
        """
       当日总成交笔数
        """
        return self._cj_data_info.total_num

    @property
    def clear_speed(self) -> ClearSpeed:
        """
       清算速度
        """
        return covert_to_enum(self._cj_data_info.clear_speed, ClearSpeed)

    @property
    def bid(self) -> list[BondQDBJInfo]:
        """
        买档
        """
        return self._qdbj_data_info['buy_info']

    @property
    def ask(self) -> list[BondQDBJInfo]:
        """
        卖档
        """
        return self._qdbj_data_info['sale_info']


class XBondOrder(BaseObject, ABC):
    def __init__(self, xbond_order_info):
        self._xbond_order_info: PXBondOrder = xbond_order_info

    @property
    def clear_speed(self) -> ClearSpeed:
        """
        清算速度
        """
        return covert_to_enum(self._xbond_order_info.clear_speed, ClearSpeed)

    @property
    def price(self) -> float:
        """
        报文生成时间
        """
        return self._xbond_order_info.price

    @property
    def ytm(self) -> float:
        """
        到期收益率
        """
        return self._xbond_order_info.ytm

    @property
    def quantity(self) -> float:
        """
        报单量
        """
        return self._xbond_order_info.quantity

    @property
    def unfilled_quantity(self) -> float:
        """
        未匹配量
        """
        return self._xbond_order_info.unfilled_quantity


class XBondInfo(BaseObject, ABC):
    def __init__(self, xbond_base_info, xbond_order_dict):
        self._xbond_base_info: PXBondBaseInfo = xbond_base_info
        self._xbond_order_dict: dict = xbond_order_dict

    @property
    def security(self) -> str:
        """
       代码
        """
        return self._xbond_base_info.security

    @property
    def datetime(self) -> float:
        """
        报文生成时间
        """
        return self._xbond_base_info.datetime

    @property
    def total_tradable_quantity(self) -> float:
        """
        可成交总量
        """
        return self._xbond_base_info.total_tradable_quantity

    @property
    def open(self) -> float:
        """
        开盘净价
        """
        return self._xbond_base_info.open

    @property
    def open_yield(self) -> float:
        """
        开盘净价收益率
        """
        return self._xbond_base_info.open_yield

    @property
    def bid(self) -> list[XBondOrder]:
        """
        买档
        """
        return self._xbond_order_dict['buy_info']

    @property
    def ask(self) -> list[XBondOrder]:
        """
        卖档
        """
        return self._xbond_order_dict['sale_info']


class YHJBondMMOrder(BaseObject, ABC):
    def __init__(self, yhj_bond_mm_order):
        self._yhj_bond_mm_order: PYHJBondMMOrder = yhj_bond_mm_order

    @property
    def quote_id(self) -> str:
        """
        报价单号
        """
        return self._yhj_bond_mm_order.quote_id

    @property
    def clear_speed(self) -> ClearSpeed:
        """
        清算速度
        """
        return covert_to_enum(self._yhj_bond_mm_order.clear_speed, ClearSpeed)

    @property
    def price(self) -> float:
        """
        净价
        """
        return self._yhj_bond_mm_order.price

    @property
    def ytm(self) -> float:
        """
        到期收益率
        """
        return self._yhj_bond_mm_order.ytm

    @property
    def full_price(self) -> float:
        """
        全价
        """
        return self._yhj_bond_mm_order.full_price

    @property
    def face_value(self) -> float:
        """
        券面总额
        """
        return self._yhj_bond_mm_order.face_value

    @property
    def settle_date(self) -> str:
        """
        结算日期
        """
        return self._yhj_bond_mm_order.settle_date

    @property
    def party_id(self) -> str:
        """
        做市方6位机构ID
        """
        return self._yhj_bond_mm_order.party_id

    @property
    def trader_id(self) -> str:
        """
        做市方交易员ID
        """
        return self._yhj_bond_mm_order.trader_id


class YHJBondMMInfo(BaseObject, ABC):
    def __init__(self, yhj_bond_mm_info, yhj_bond_mm_order_dict):
        self._yhj_bond_mm_info: PYHJBondMMInfo = yhj_bond_mm_info
        self._yhj_bond_mm_order_dict: dict = yhj_bond_mm_order_dict

    @property
    def security(self) -> str:
        """
       代码
        """
        return self._yhj_bond_mm_info.security

    @property
    def datetime(self) -> float:
        """
        报文生成时间
        """
        return self._yhj_bond_mm_info.datetime

    @property
    def bid(self) -> list[YHJBondMMOrder]:
        """
        买档
        """
        return self._yhj_bond_mm_order_dict['buy_info']

    @property
    def ask(self) -> list[YHJBondMMOrder]:
        """
        卖档
        """
        return self._yhj_bond_mm_order_dict['sale_info']


class BondCalcData(BaseObject, ABC):
    def __init__(self):
        self._security: str = ""
        self._date: str = ""
        self._full_price: float = 0
        self._net_price: float = 0
        self._ytm: float = 0
        self._ytc: float = 0
        self._yield_error: str = ""

    @property
    def security(self) -> str:
        """
       代码
        """
        return self._security

    @security.setter
    def security(self, value):
        self._security = value

    @property
    def date(self) -> str:
        """
        定价日期
        """
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def full_price(self) -> float:
        """
        全价
        """
        return self._full_price

    @full_price.setter
    def full_price(self, value):
        self._full_price = value

    @property
    def net_price(self) -> float:
        """
        净价
        """
        return self._net_price

    @net_price.setter
    def net_price(self, value):
        self._net_price = value

    @property
    def ytm(self) -> float:
        """
        到期收益率
        """
        return self._ytm

    @ytm.setter
    def ytm(self, value):
        self._ytm = value

    @property
    def ytc(self) -> float:
        """
        行权收益率
        """
        return self._ytc

    @ytc.setter
    def ytc(self, value):
        self._ytc = value

    @property
    def yield_error(self) -> str:
        """
        收益率问题
        """
        return self._yield_error

    @yield_error.setter
    def yield_error(self, value):
        self._yield_error = value

class GroupMsgData(BaseObject,ABC):
    def __init__(self, PGroupParamData):
        from qt_strategy_base.core.model.model import PGroupMsgData
        self._data:PGroupParamData= PGroupParamData
        if  self._data.type_name=="I":
            self._value=int(self._data.data)
            return
        if self._data.type_name=="S":
            self._value= str(self._data.data)
            return
        if self._data.type_name=="D":
            self._value = float(self._data.data)
            return

        self._value=base64.b64decode(self._data.data)

    @property
    def group_id(self)->int:
        """
        消息标识
        @return:
        """
        return self._data.group_id

    @property
    def key(self)->str:
        """
        值
        @return:
        """
        return self._data.key

    @property
    def length(self) ->int:
        """
        消息标识
        @return:
        """
        return self._data.length

    @property
    def index(self) -> int:
        """
        消息编号
        @return:
        """
        return self._data.index

    @property
    def type_name(self) -> str:
        """
        参数类型
        @return:
        """
        return self._data.type_name

    @property
    def time_stamp(self) -> float:
        """
        消息的发送时间
        @return:
        """
        return self._data.time_stamp

    @property
    def group_name(self) -> str:
        """
        消息的发送时间
        @return:
        """
        return self._data.group_name

    @property
    def data(self) ->any:
        """
        消息的类型，除了"I","D","S"，剩下的都是byte数组
        @return:
        """
        return self._value



