# -*- coding: utf-8 -*-
from dataclasses import dataclass


@dataclass
class PSnapshotData:
    security: str  # 代码
    high: float  # 最高价
    open: float  # 开盘价
    low: float  # 最低价
    last: float  # 最新价
    limit_up: float  # 涨停价
    limit_down: float  # 跌停价
    volume: float  # 交易量
    value: float  # 交易金额
    pre_close: float  # 昨收价
    settlement: float  # 结算价
    open_interest: float  # 持仓量
    pre_settlement: float  # 昨结价
    status: int  # 行情状态
    time: int  # 时间戳
    iopv: float  # 基金净值
    bid_price: list  # 买档价格
    bid_amount: list  # 买档价格
    ask_price: list  # 卖档价格
    ask_amount: list  # 卖档价格

    def __post_init__(self):
        self.bid = list(zip(self.bid_price, self.bid_amount))
        self.ask = list(zip(self.ask_price, self.ask_amount))


@dataclass
class PNeeqSnapshotData:
    security: str  # 代码
    maker_time: int  # 做市商行情时间
    investor_time: int  # 投资者行情时间
    order_buy_price_list: list  # 做市商买档
    order_sell_price_list: list  # 做市商卖档
    order_buy_amount_list: list  # 做市商买档
    order_sell_amount_list: list  # 做市商卖档
    level_buy_price_list: list  # 投资者买档
    level_sell_price_list: list  # 投资者卖档
    level_buy_amount_list: list  # 投资者买档
    level_sell_amount_list: list  # 投资者卖档

    def __post_init__(self):
        self.investor_bid = list(zip(self.level_buy_price_list, self.level_buy_amount_list))
        self.investor_ask = list(zip(self.level_sell_price_list, self.level_sell_amount_list))
        self.maker_bid = list(zip(self.order_buy_price_list, self.order_buy_amount_list))
        self.maker_ask = list(zip(self.order_sell_price_list, self.order_sell_amount_list))


@dataclass
class PBarData:
    security: str  # 代码
    date: str  # 日期
    time: str  # 时间
    open: float  # 开盘价
    low: float  # 最低价
    high: float  # 最新价
    close: float  # 收盘价
    pre_close: float  # 昨收价
    volume: float  # 成交量
    value: float  # 成交额


@dataclass
class POrderData:
    id: int  # 委托编号
    security: str  # 代码
    datetime: str  # 委托时间
    price: float  # 委托价格
    quantity: float  # 委托数量
    side: int  # 委托方向
    direction: int  # 开平方向
    close_type: int  # 平仓类型
    status: int  # 委托状态
    invest_type: int  # 投资类型
    internal_id: str  # 内部委托号
    revoke_cause: str  # 委托拒绝/委托撤废等原因
    cancel_value: float  # 撤单数量
    cancel_quantity: float  # 撤单数量
    investunit_id: int  # 投资单元ID
    portfolio_id: int  # 投资组合 ID
    filled_quantity: float  # 成交数量
    filled_value: float  # 成交金额
    remark: str  # 备注
    scheme_id: int  # 方案号
    security_detail_id: str  # 方案明细号
    operator_no: int  # 操作员号
    is_nicked: int  # 是否匿名
    clear_speed: int  # 清算速度
    counterparty_order_id: str  # 对手方报价编号
    trade_type: int  # 交易所债券点价交易方式


@dataclass
class PCombOrderData:
    security: str  # 代码
    id: int  # 委托编号
    datetime: str  # 委托时间
    status: int  # 委托状态
    buy_price: float  # 买方向委托价格
    sell_price: float  # 卖方向委托价格
    buy_quantity: float  # 买方向委托数量
    sell_quantity: float  # 卖方向委托数量
    buy_cancel_quantity: float  # 买方向撤单数量
    sell_cancel_quantity: float  # 卖方向撤单数量
    buy_direction: int  # 买方向的开平方向
    sell_direction: int  # 卖方向的开平方向
    buy_close_type: int  # 买方向的平仓类型
    sell_close_type: int  # 卖方向的平仓类型
    buy_id: int  # 买方向委托序号(外部委托)
    sell_id: int  # 卖方向委托序号(外部委托)
    buy_status: int  # 买方向委托状态
    sell_status: int  # 卖方向委托状态
    internal_id: str  # 内部委托号
    invest_type: int  # 投资类型
    revoke_cause: str  # 废单原因
    investunit_id: int  # 账户 ID
    portfolio_id: int  # 投资组合 ID
    buy_filled_quantity: float  # 买方向成交数量
    sell_filled_quantity: float  # 卖方向成交数量
    buy_filled_value: float  # 买方向成交金额
    sell_filled_value: float  # 卖方向成交金额
    remark: str  # 备注消息
    scheme_id: int  # 方案号
    security_detail_id: str  # 方案明细号
    operator_no: int  # 操作员号


@dataclass
class PTradeData:
    security: str  # 代码
    id: int  # 成交编号
    datetime: str  # 成交时间
    volume: float  # 成交数量
    value: float  # 成交金额
    order_quantity: float  # 委托数量
    side: int  # 委托方向
    direction: int  # 开平方向
    close_type: int  # 平仓方向
    internal_id: str  # 内部委托号
    order_id: int  # 外部委托编号
    invest_type: int  # 投资类型
    fee: float  # 当次费用
    total_volume: float  # 累计成交数量
    total_value: float  # 累计成交金额
    remark: str  # 备注
    investunit_id: int  # 账户 ID
    portfolio_id: int  # 投资组合 ID
    scheme_id: int  # 方案号
    security_detail_id: str  # 方案明细号


@dataclass
class PPositionData:
    security: str  # 代码
    invest_type: int  # 投资类型
    position_type: int  # 多空类型
    initial_position: float  # 期初数量
    position: float  # 当前持仓数量
    available_position: float  # 可用数量
    yesterday_available_position: float  # 昨仓可用数量
    today_available_position: float  # 今仓可用
    buy_volume: float  # 当日买成交数量
    buy_value: float  # 当日买成交金额
    sell_volume: float  # 当日卖成交数量
    sell_value: float  # 当日卖成交金额
    unfilled_order_buy_quantity: float  # 买挂单数量
    unfilled_order_sell_quantity: float  # 卖挂单数量
    frozen_quantity: float  # 冻结数量
    cost: float  # 持仓成本
    total_fee: float  # 持仓费用
    investunit_id: int  # 账户 ID
    portfolio_id: int  # 投资组合 ID
    etf_purchase_quantity: float  # etf申购成交数量
    etf_redeem_quantity: float  # etf赎回成交数量


@dataclass
class PMarketDutyData:
    security: str  # 代码
    optimal_buy_value: float  # 最优买金额
    optimal_sell_value: float  # 最优卖金额
    optimal_buy_quantity: float  # 最优买量
    optimal_sell_quantity: float  # 最优卖量
    max_buy_price: float  # 最高买入价
    min_sell_price: float  # 最低卖出价
    min_spread_rate: float  # 最小报价差比
    optimal_spread: float  # 最优价差
    buy_volume: float  # 买成交数量
    sell_volume: float  # 卖成交数量
    open_auction_quote_flag: str  # 开盘集合竞价时段报价标识
    avg_declared_value: float  # 平均每笔申报金额
    valid_duration: int  # 做市有效时长
    exempt_duration: int  # 做市豁免时长
    suspended_duration: int  # 停牌时长
    exempt_status: str  # 豁免状态
    current_invalid_duration: int  # 当前无效时长
    today_invalid_duration: int  # 当日无效时长
    current_market_time_rate: float  # 当前做市时间比例
    today_market_time_rate: float  # 当日做市时间比例
    is_satisfy_market_duty: str  # 是否满足做市义务
    TWAP_spread: float  # 时间加权平均买卖价差
    buy_quantity: float  # 买方向委托数量
    sell_quantity: float  # 卖方向委托数量
    adjust_time: int  # 调整时间
    business_classification: str  # 业务分类
    TWAP_spread_rate: float  # 时间加权平均买卖价差率
    total_spread_rate: float  # 累计买卖价差比
    close_participation_rate: float  # 收盘集合竞价参与率
    open_participation_rate: float  # 开盘集合竞价参与率
    trading_curb_participation_rate: float  # 熔断集合竞价参与率


@dataclass
class PSecurityBaseInfo:
    security: str  # 代码
    security_type: int  # 证券类型
    buy_unit: int  # 买单位
    sell_unit: int  # 卖单位
    buy_qty_max: float  # 最大买入数量
    sell_qty_max: float  # 最大卖出数量
    market_buy_qty_max: float  # 最大市价买入数量
    market_sell_qty_max: float  # 最大市价卖出数量
    contract_multiplier: int  # 合约乘数
    minimal_price_spread: float  # 最小买卖价差
    buy_qty_min: float  # 最小买入数量
    sell_qty_min: float  # 最小卖出数量
    board_type: int  # 板块
    total_shares: float  # 总股本
    outstanding_shares: float  # 流通股本
    scheme_ins_serial_no: str  # 明细号


@dataclass
class PStockBaseInfo:
    security: str  # 代码
    security_type: int  # 证券类型
    buy_unit: int  # 买单位
    sell_unit: int  # 卖单位
    buy_qty_max: float  # 最大买入数量
    sell_qty_max: float  # 最大卖出数量
    market_buy_qty_max: float  # 最大市价买入数量
    market_sell_qty_max: float  # 最大市价卖出数量
    contract_multiplier: int  # 合约乘数
    minimal_price_spread: float  # 最小买卖价差
    buy_qty_min: float  # 最小买入数量
    sell_qty_min: float  # 最小卖出数量
    board_type: int  # 板块
    total_shares: float  # 总股本
    outstanding_shares: float  # 流通股本


@dataclass
class PBondBaseInfo:
    security: str  # 代码
    security_type: int  # 证券类型
    buy_unit: int  # 买单位
    sell_unit: int  # 卖单位
    buy_qty_max: float  # 最大买入数量
    sell_qty_max: float  # 最大卖出数量
    market_buy_qty_max: float  # 最大市价买入数量
    market_sell_qty_max: float  # 最大市价卖出数量
    contract_multiplier: int  # 合约乘数
    minimal_price_spread: float  # 最小买卖价差
    buy_qty_min: float  # 最小买入数量
    sell_qty_min: float  # 最小卖出数量
    board_type: int  # 板块
    total_shares: float  # 总股本
    outstanding_shares: float  # 流通股本
    face_value: float  # 面值
    interests: float  # 百元债券利息
    change_price: float  # 转股价
    remaining_term: float  # 剩余期限（年）


@dataclass
class PFuturesBaseInfo:
    security: str  # 代码
    security_type: int  # 证券类型
    buy_unit: int  # 买单位
    sell_unit: int  # 卖单位
    buy_qty_max: float  # 最大买入数量
    sell_qty_max: float  # 最大卖出数量
    market_buy_qty_max: float  # 最大市价买入数量
    market_sell_qty_max: float  # 最大市价卖出数量
    contract_multiplier: int  # 合约乘数
    minimal_price_spread: float  # 最小买卖价差
    buy_qty_min: float  # 最小买入数量
    sell_qty_min: float  # 最小卖出数量
    board_type: int  # 板块
    total_shares: float  # 总股本
    outstanding_shares: float  # 流通股本
    last_trade_date: int  # 最后交易日期
    last_trade_time: int  # 最后交易时间
    settlement_month: int  # 交割年月
    settlement_date: int  # 交割日期


@dataclass
class POptionBaseInfo:
    security: str  # 代码
    security_type: int  # 证券类型
    buy_unit: int  # 买单位
    sell_unit: int  # 卖单位
    buy_qty_max: float  # 最大买入数量
    sell_qty_max: float  # 最大卖出数量
    market_buy_qty_max: float  # 最大市价买入数量
    market_sell_qty_max: float  # 最大市价卖出数量
    contract_multiplier: int  # 合约乘数
    minimal_price_spread: float  # 最小买卖价差
    buy_qty_min: float  # 最小买入数量
    sell_qty_min: float  # 最小卖出数量
    board_type: int  # 板块
    total_shares: float  # 总股本
    outstanding_shares: float  # 流通股本
    underlying: str  # 标的代码
    type: int  # 期权类型
    exercise_type: int  # 行权类型
    strike_price: float  # 行权价
    begin_trade_date: int  # 开始交易日期
    end_trade_date: int  # 结束交易日期
    exercise_begin_date: int  # 行权起始日期
    exercise_end_date: int  # 行权结束日期
    exercise_month: int  # 到期月份






@dataclass
class PAccountInfo:
    investunit_id: int  # 投资单元id
    portfolio_id: int  # 投资组合id
    name: str  # 账户名称


@dataclass
class PETFInfo:
    security: str  # 代码
    stock_num: float  # 获取成分股数量
    minimal_subscribe_unit: int  # 获取ETF申报单位
    max_cash_rep_ratio: float  # 获取现金比例上限
    publish_type: int  # 信息发布标志
    status: int  # 当天状态
    estimated_cash_balance: float  # t日预估现金余额
    market_type: int  # ETF类型
    constituent_type: int  # ETF成分股类型
    sub_red_type: int  # ETF申赎类型
    pre_nav: float  # 获取基金昨日单位净值
    pre_unit_nav:float #基金单位净值


@dataclass
class PETFConstituent:
    security: str  # 证券代码
    quantity: float  # 数量
    cash_rep_type: int  # 现金替代标志
    subscribe_rep_premium_ratio: float  # 申购现金替代溢价比率
    redeem_rep_discount_ratio: float  # 赎回现金替代折价比率
    subscribe_rep_value: float  # 申购替代金额
    redeem_rep_value: float  # 赎回替代金额


@dataclass
class PSecurityDetail:
    id: int  # 证券明细号
    security: str  # 证券明细代码
    side: int  # 委托方向
    direction: int  # 开平方向
    close_type: int  # 平仓类型
    target_value: float  # 目标金额
    target_quantity: float  # 目标数量
    control_type: int  # 控制类型
    limit_price: float  # 价格限制
    total_volume: float  # 累计成交数量
    total_value: float  # 累计成交金额
    status: int  # 明细状态
    order_quantity: float  # 累计委托数量
    order_value: float  # 累计委托金额

    investunit_id: int
    invest_type: str
    portfolio_id: int


@dataclass
class PAccountFund:
    T0_balance: float
    T1_balance: float
    margin_available: float  # 保证金可用
    margin_occupy: float  # 保证金占用
    margin_balance: float
    margin_unfilled_order_occupy: float




@dataclass
class PBalanceAndAmount:
    entrust_direction_out: int
    entrust_amount: float  # 买单位
    entrust_balance: float  # 卖单位
    deal_amount: float  # 最大买入数量
    deal_balance: float  # 最大卖出数量


@dataclass
class PStockDetailInfo:
    scheme_ins_serial_no: str  # 代码
    real_deal_dir: int  # 证券类型
    entrust_amount: int  # 买单位
    entrust_balance: int  # 卖单位
    deal_amount: float  # 最大买入数量
    deal_balance: float  # 最大卖出数量


@dataclass
class PFactor:
    security: str  # 代码
    factor_name: str  # 因子名称
    factor_value: float  # 因子值
    time_stamp: float  # 更新时间


@dataclass
class PAlgoStrategy:
    strategy_id: int  # 策略id
    strategy_name: str  # 策略名称
    busin_class_list: list  # 支持的业务类
    market_no_list: list  # 支持的市场列表
    entrdirection_list: list  # 支持的委托方向列表
    stock_ctrl_type: list  # 支持的控制类型列表


@dataclass
class PAlgoScheme:
    scheme_id: int  # 策略id
    scheme_name: str  # 策略名称
    scheme_status: int  # 方案状态
    control_type: int  # 方案控制类型
    param_value_list: str  # 参数


@dataclass
class PAlgoStrategyParamInfo:
    name: str  # 参数名称
    type: str  # 参数类型


@dataclass
class PAlgoDetail:
    scheme_id: int  # 方案ID
    id: str  # 证券明细号
    security: str  # 证券明细代码
    side: int  # 委托方向
    direction: int  # 开平方向
    target_value: float  # 目标金额
    target_quantity: float  # 目标数量
    control_type: int  # 控制类型
    limit_price: float  # 价格限制
    total_volume: float  # 累计成交数量
    total_value: float  # 累计成交金额
    status: int  # 明细状态
    order_quantity: float  # 累计委托数量
    order_value: float  # 累计委托金额
    investunit_id: int
    invest_type: str
    portfolio_id: int
    third_remark: str


@dataclass
class PQDBJHqInfo:
    security: str
    level_no: int
    order_id: str
    quote_time: int
    net_price: float
    quantity: float
    quoter: str
    clear_speed: int


@dataclass
class PCJHqInfo:
    security: str
    datetime: int
    open: float
    high: float
    low: float
    last: float
    wwap: float
    pre_close: float
    pre_vwap: float
    open_yield: float
    high_yield: float
    low_yield: float
    last_yield: float
    vwap_yield: float
    pre_close_yield: float
    pre_vwap_yield: float
    volume: float
    total_volume: float
    total_value: float
    total_num: float
    clear_speed: int


@dataclass
class PXBondBaseInfo:
    security: str
    datetime: float
    total_tradable_quantity: float
    open: float
    open_yield: float
    clear_speed: int

@dataclass
class PXBondOrder:
    clear_speed: float
    price: float
    ytm: float
    quantity: float
    unfilled_quantity: float


@dataclass
class PYHJBondMMInfo:
    security: str
    symbol: str
    datetime: float
    clear_speed: int


@dataclass
class PYHJBondMMOrder:
    quote_id: str
    clear_speed: int
    price: float
    ytm: float
    full_price: float
    face_value: float
    clear_type: int
    settle_date: str
    settle_type: int
    party_id: str
    trader_id: str


@dataclass
class PBondPricing:
    security: str
    date: str
    full_price: float
    net_price: float
    ytm: float
    ytc: float
    yield_error: str

@dataclass
class PGroupMsgData:
    key:str
    data:str
    length:int
    index:int
    type_name:str
    time_stamp:float
    group_name:str
    group_id:int
    scheme_id:int

