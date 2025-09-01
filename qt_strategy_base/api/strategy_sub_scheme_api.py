# -- coding: utf-8 --
from typing import Tuple, List

from qt_strategy_base.core.cache.sub_scheme_manage import SubSchemeManager
from qt_strategy_base.model.algo_detail import AlgoDetail
from qt_strategy_base.model.algo_scheme import AlgoScheme
from qt_strategy_base.model.enum import ControlType
from qt_strategy_base.model.error_info import ErrorInfo


class SchemeManager:
    @staticmethod
    def create_scheme(strategy_id: int, control_type: ControlType) -> Tuple[ErrorInfo, AlgoScheme]:
        return SubSchemeManager().create_scheme(strategy_id=strategy_id, control_type=control_type)

    @staticmethod
    def get_security_details() -> List[AlgoDetail]:
        return SubSchemeManager().get_security_details()

    @staticmethod
    def get_all_scheme() -> List[AlgoScheme]:
        return SubSchemeManager().get_all_scheme()
