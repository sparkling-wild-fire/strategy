# -*- coding: utf-8 -*-
from enum import Enum


# 证券类别
class SecurityType(Enum):
    STOCK = 1  # 股票
    CLOSED_ENDED_FUND = 2  # 封闭式基金
    TREASURY = 3  # 国债
    ENTERPRISE_BOND = 4  # 企债
    CONVERTIBLE_BOND = 5  # 可转债
    POLICY_FINANCIAL_BOND = 6  # 政策性金融债
    OPEN_ENDED_FUND = 11  # 开放式基金
    FINANCIAL_BOND = 12  # 非政策性金融债
    SUB_BOND = 16  # 次级债
    STOCK_INDEX_FUTURES = 23  # 股指期货
    CORPORATE_BOND = 24  # 公司债
    MUNICIPAL_BOND = 25  # 地方债
    CDR = 27  # CDR
    TREASURY_FUTURES = 28  # 国债期货
    STOCK_SUB = 33  # 股票申购
    BOND_SUB = 42  # 债券申购
    CTA = 50  # 商品期货
    CALL_OPTION = 60  # 认购期权
    PUT_OPTION = 61  # 认沽期权
    BOND_REPURCHASE = 63  # 债券回购
    REITS = 155  # REITS基金
    REITS_SUB = 156  # REITS基金认购


# 行情状态
class SnapshotStatus(Enum):
    Trade = 3  # 交易(连续撮合)
    Suspend = 5  # 停盘
    TemporarySuspend = 11  # 临时停盘


# 定时器类型
class ScheduleType(Enum):
    FIXED = 0  # 固定时间运行
    INTERVAL = 1  # 固定间隔运行


# 设置类型
class Setting(Enum):
    SHOW_FINISHED_ORDER = 0  # 展示终态委托
    REPEAT_CANCEL = 1  # 撤单失败时重试


# 复权类型
class AdjustType(Enum):
    PRE = 0  # 前复权
    POST = 1  # 后复权
    nan = 2  # 不调整


# 账户类型
class AccountType(Enum):
    ORDINARY_ACCOUNT = 1  # 普通账户
    MARGIN_ACCOUNT = 2  # 保证金账户


# 买卖方向
class Side(Enum):
    BUY = 1  # 买入
    SELL = 2  # 卖出
    PURCHASE = 20  # 申购
    REDEEM = 21  # 赎回


# 委托状态
class OrderStatus(Enum):
    UNREPORT = 1  # 未报
    TOREPORT = 2  # 待报
    REPORTING = 3  # 正报
    CONFIRM = 4  # 已报
    WASTE = 5  # 废单
    PARTFILLED = 6  # 部成
    FILLED = 7  # 已成
    PARTCANCELLED = 8  # 部撤
    CANCELLED = 9  # 已撤
    CANCELLING = 49  # 待撤


# 板块枚举
class BoardType(Enum):
    MAIN = 0  # 主板
    STAR = 1  # 科创板
    SME = 2  # 中小板
    GEM = 3  # 创业板


# 委托状态
class PushType(Enum):
    ORDER_FAIL = 0  # 委托废单
    ORDER_RECEIVE = 1  # 委托下达
    ORDER_CONFIRM = 2  # 委托确认
    CANCEL_CONFIRM = 3  # 撤成
    CANCEL_RECEIVE = 4  # 撤单
    CANCEL_FAIL = 5  # 撤废
    TRADE_RECEIVE =6  #成交


# 信息发布标志
class ETFPublishType(Enum):
    NO_PUBLISH = 0  # 不发布
    PUBLISH = 1  # 发布
    PUBLISH_NOCAL = 2  # 发布（交易所不计）


# 基金运行状态
class ETFStatus(Enum):
    OPEN = 1  # 开放申购赎回
    CLOSE = 0  # 不开放申购赎回
    SUBSCRIBE_ONLY = 2  # 仅申购
    REDEEM_ONLY = 3  # 仅赎回


# 现金替代类型
class ETFCashReplaceType(Enum):
    CASH_REP = 1  # 可替代
    CASH_UNREP = 0  # 不可替代
    CASH_FORCE = 2  # 必须替代
    SZ_CASH_REP = 3  # 深市退补现金替代
    SZ_CASH_FORCE = 4  # 深市必须现金替代
    HK_CASH_REP = 7  # 港市退补现金替代
    HK_CASH_FORCE = 8  # 港市必须现金替代
    CB_CASH_REP = 5  # 跨境退补现金替代（非沪深退补现金替代）
    CB_CASH_FORCE = 6  # 跨境必须现金替代（非沪深必须现金替代）


# 明细控制类别
class ControlType(Enum):
    NO_CONTROL = 0  # 不控制
    VALUE_CONTROL = 1  # 按金额控制
    QUANTITY_CONTROL = 2  # 按数量控制


# 证券明细执行状态
class SecurityDetailStatus(Enum):
    RUNNING = 0  # 运行中
    PAUSED = 1  # 已暂停
    CANCELLED = 2  # 已撤销
    FINISHED = 3  # 已完成
    EXPIRED = 4  # 已过期
    CANCELLING = 5  # 撤销中


# 期权行权方式
class OptionExerciseType(Enum):
    EUROPEAN_STYLE = 1  # 欧式
    AMERICAN_STYLE = 2  # 美式
    BERMUDA_STYLE = 3  # 百慕大


# 交易市场
class Market(Enum):
    XSHG = "XSHG"  # 上交所
    XSHE = "XSHE"  # 深交所
    XSGE = "XSGE"  # 上期所
    XZCE = "XZCE"  # 郑商所
    CCFX = "CCFX"  # 中金所
    XDCE = "XDCE"  # 大商所
    NEEQ = "NEEQ"  # 股转
    XGFE = "XGFE"  # 广期所
    XINE = "XINE"  # 能源交易中心


# 对外委托方向定义
class DirectionOut(Enum):
    NONE = 0  # 不区分
    BUY = 1  # 买入
    SALE = 2  # 卖出
    BUY_OPEN = 3  # 买入开仓
    SALE_CLOSE = 4  # 卖出平仓
    SALE_OPEN = 5  # 卖出开仓
    BUY_CLOSE = 6  # 买入平仓
    COLLATERAL_BUY = 7  # 担保品买入
    COLLATERAL_SELL = 8  # 担保品卖出
    FINANCE_BUY = 9  # 融资买入
    FINANCE_SELL = 10  # 融券卖出
    MARGIN_BUY = 11  # 买券还券
    MARGIN_SELL = 12  # 卖券还款
    ETF_APPLY = 13  # ETF申购
    ETF_REDEEM = 14  # ETF赎回


# 开平方向
class Direction(Enum):
    OPEN = 1  # 开仓
    CLOSE = 2  # 平仓


# 开平仓类型
class CloseType(Enum):
    TODAY = 1  # 平今仓
    YESTERDAY = 2  # 平昨仓


# 投资类型
class InvestType(Enum):
    SPECULATE = 49  # 投机【商品期货和商品期权的默认字段】
    HEDGE = 50  # 套保
    ARBITRAGE = 51  # 套利
    TRADABLE = 1  # 可交易【股票和ETF期权默认字段】


# 成份股类型
class ETFConstituentType(Enum):
    STOCK = 1  # 股票
    BOND = 2  # 债券
    GOLD = 3  # 黄金
    TRADABLE_MONEY_FUND = 4  # 交易型货币基金
    OPEN_MONEY_FUND = 5  # 申赎型货币基金


# ETF市场类型
class ETFMarketType(Enum):
    LOCAL = 1  # 本市场ETF
    CROSS_BOARD = 2  # 跨境ETF
    CROSS_MARKET = 3  # 跨市场ETF
    CROSS_ZD = 4  # 跨市场（中登）


# 申赎类型
class SubNRedType(Enum):
    GENERAL = 0  # 普通
    CASH = 1  # 现金
    PHYSICAL = 2  # 实物


# 持仓类型
class PositionType(Enum):
    LONG = 1  # 多仓
    SHORT = 2  # 空仓
    COVEREDSHORT = 50  # 备兑空仓
    POWER = 55  # 权利仓
    DUTY = 56  # 义务仓


# 期权类型
class OptionType(Enum):
    CALL = 1  # 认购
    PUT = 2  # 认沽


# 方案执行状态
class SchemeType(Enum):
    UNINIT = 0  # 未初始化
    RUNNING = 1  # 运行中
    PAUSED = 2  # 已暂停
    CANCELLED = 3  # 已撤销
    FINISHED = 4  # 已完成
    EXPIRED = 5  # 已过期
    CANCELLING = 6  # 撤销中


# 对外委托方向定义
class EntrustDirectionOut(Enum):
    NONE = 1  # 不区分
    BUY = 2  # 买入
    SALE = 3  # 卖出
    BUY_OPEN = 4  # 买入开仓
    SALE_CLOSE = 5  # 卖出平仓
    SALE_OPEN = 6  # 卖出开仓
    BUY_CLOSE = 7  # 买入平仓
    COLLATERAL_BUY = 8  # 担保品买入
    COLLATERAL_SELL = 9  # 担保品卖出
    FINANCE_BUY = 10  # 融资买入
    FINANCE_SELL = 11  # 融券卖出
    MARGIN_BUY = 12  # 买券还券
    MARGIN_SELL = 13  # 卖券还款


class MessageType(Enum):
    ERROR = 1  # 错误
    WARN = 2  # 警告
    INFO = 3  # 提示


class ExecuteMode(Enum):
    Run = 0
    Debug = 1


class ClearSpeed(Enum):
    T0 = 0  # T+0
    T1 = 1  # T+1


class TradeType(Enum):
    DEFAULT = 0  # 允许部分成交
    FOK = 1  # 全额成交


class SettleType(Enum):
    PAD = 0  # 见券付款
    DAP = 1  # 见款付券
    DVP = 2  # 券款对付


class ClearType(Enum):
    FULL = 0  # 全额
    NET = 1  # 净额
