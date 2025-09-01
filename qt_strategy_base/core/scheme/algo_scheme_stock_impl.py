# -- coding: utf-8 --
# -*- coding: utf-8 -*-
import uuid

from qt_strategy_base.core.common.public_func import covert_to_enum
from qt_strategy_base.core.model.model import PAlgoDetail
from qt_strategy_base.model.algo_detail import AlgoDetail
from qt_strategy_base.model.enum import Side, Direction, ControlType, SecurityDetailStatus
from qt_strategy_base.model.strategy_api_data import AccountInfo


class AlgoDetailImpl(AlgoDetail):

    def __init__(self):
        self._id: str = ""  # 证券明细号
        self._security: str = ""  # 证券明细代码
        self._account: AccountInfo = None  # 证券明细代码
        self._side: Side = None  # 委托方向
        self._direction: Direction = None  # 开平方向
        self._target_value: float = 0  # 目标金额
        self._target_quantity: float = 0  # 目标数量
        self._ctrl_type: ControlType = ControlType.NO_CONTROL  # 按金额控制和按数量控制
        self._limit_price: float = 0  # 价格限制
        self._total_volume: float = 0  # 累计成交数量
        self._total_value: float = 0  # 累计成交金额
        self._order_quantity: float = 0  # 累计委托数量
        self._order_value: float = 0  # 累计委托金额
        self._scheme_stock_status: SecurityDetailStatus = SecurityDetailStatus.RUNNING  # 明细状态
        self._third_remark: str = ""

    @staticmethod
    def gather_scheme_stocks_info(security: str, ctrl_type, account_info: AccountInfo, side: Side,
                                  direction: Direction, target_quantity: float, target_value: float):
        ret = AlgoDetailImpl()
        ret._third_remark = str(uuid.uuid4())
        ret._security = security
        ret._ctrl_type = ctrl_type
        ret._account = account_info
        ret._side = side
        ret._direction = direction
        ret._target_value = target_value
        ret._target_quantity = target_quantity

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
    def target_value(self) -> float:
        """
        目标金额
        """
        return self._target_value

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

    @property
    def third_remark(self) -> str:
        """
        本地明细标志
        """
        return self._third_remark

    def get_account(self) -> AccountInfo:
        return self._account

    def update_value(self, algo_detail: PAlgoDetail):
        self._total_volume: float = algo_detail.total_volume
        self._total_value: float = algo_detail.total_value
        self._order_quantity: float = algo_detail.order_quantity
        self._order_value: float = algo_detail.order_value
        self._scheme_stock_status: SecurityDetailStatus = covert_to_enum(algo_detail.status, SecurityDetailStatus)
        if self._account is None:

            self._id: str = algo_detail.id  # 证券明细号
            self._side: Side = algo_detail.side  # 委托方向
            self._direction: Direction = algo_detail.direction  # 开平方向
            self._limit_price: float = algo_detail.limit_price
            self._third_remark: str = ""
            self._account= AccountInfo(investunit_id=algo_detail.investunit_id,invest_type=1,portfolio_id=algo_detail.portfolio_id)
            self._security= algo_detail.security
