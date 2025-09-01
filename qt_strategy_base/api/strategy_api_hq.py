# -*- coding: utf-8 -*-
from typing import List, Tuple, Dict

from qt_strategy_base import ClearSpeed
from qt_strategy_base.core.common.aglo_function_impl import FunctionImpl
from qt_strategy_base.model.error_info import ErrorInfo
from qt_strategy_base.model.strategy_api_data import SnapshotData, NeeqSnapshotData, BondClickHq


def get_snapshot(security_list: list[str]) -> Tuple[ErrorInfo, Dict[str, SnapshotData]]:
    """
    快照行情查询
    @param security_list: 券的列表，如["600570.XSHG","600000.XSHG"]
    @return:错误信息、主键为证券名称值为SnapshotData字典
    """
    return FunctionImpl.get_snapshot(security_list=security_list)


def get_neeq_snapshot(security_list: list[str]) -> Tuple[ErrorInfo, Dict[str, NeeqSnapshotData]]:
    """
    股转快照行情查询
    @param security_list: 券的列表，如["600570.XSHG","600000.XSHG"]
    @return::错误信息、主键为证券名称值为NeeqSnapshotData字典
    """
    return FunctionImpl.get_neeq_snapshot(security_list=security_list)
