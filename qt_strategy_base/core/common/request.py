# -*- coding: utf-8 -*-
from typing import List, Any

from qt_strategy_base.core.common.constant import FunctionID


def make_request_no_recv(scheme_id: int, function_id: FunctionID, fields: List[str], data: List[Any]):
    """
    异步请求
    @param scheme_id: 方案号
    @param function_id: 功能号
    @param fields: 列头
    @param data: 值
    @return:None
    """
    from qt_strategy_base.core.tcp_client import TcpClient
    TcpClient().make_request_no_recv(scheme_id=scheme_id, function_id=function_id.value, fields=fields, data=data)


def make_request(function_id: FunctionID, fields: List[str], data: List[Any], scheme_id: int = 0) -> Any:
    """
    同步请求
    @param function_id:功能号
    @param fields:列头
    @param data:值
    @param scheme_id:方案号 默认为0，后续会填入当前线程正在处理的方案号
    @return:答应包
    """
    from qt_strategy_base.core.tcp_client import TcpClient
    return TcpClient().make_request(scheme_id=scheme_id, function_id=function_id.value, fields=fields, data=data)


def make_request2(function_id: FunctionID, request_params: dict, scheme_id: int = 0) -> Any:
    """
    同步请求
    @param function_id: 功能号
    @param request_params: 参数包
    @param scheme_id: 方案号 默认为0，后续会填入当前线程正在处理的方案号
    @return:
    """
    from qt_strategy_base.core.tcp_client import TcpClient
    return TcpClient().make_request2(scheme_id=scheme_id, function_id=function_id.value, request_params=request_params)


def make_response_no_recv(scheme_id: int, function_id: FunctionID, package_id: int, fields: List[str], data: List[Any]):
    """
    应达
    @param scheme_id: 方案号
    @param function_id: 功能号
    @param package_id: 包id
    @param fields: 列头
    @param data: 值
    @return:None
    """
    from qt_strategy_base.core.tcp_client import TcpClient
    TcpClient().make_response_no_recv(scheme_id=scheme_id, function_id=function_id.value, package_id=package_id,
                                      fields=fields, data=data)
