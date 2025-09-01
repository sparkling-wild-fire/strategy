# -*- coding: utf-8 -*-
import io
from typing import Any, Tuple

import numpy as np
import pandas as pd
from pandas import DataFrame

from qt_strategy_base.model.error_info import ErrorInfo


def covert_data_to_class_list(data_items: list, fields: list, data_class: Any) -> Any:
    result_list = []
    for data_item in data_items:
        data_dict = dict(zip(fields, data_item))
        data_info = data_class(**data_dict)
        result_list.append(data_info)
    return result_list


def covert_message_to_p_class_tuple(msg: dict, data_name: str, data_class: Any) -> Tuple[
    ErrorInfo, Any]:
    error_info = ErrorInfo(msg['error_no'], msg['error_msg'])
    data_item = msg['body'][data_name].get('data', None)
    fields = msg['body'][data_name].get('fields', None)
    if data_item is None or fields is None:
        return error_info, None
    data_dict = dict(zip(fields, data_item))
    data_info = data_class(**data_dict)
    return error_info, data_info


def covert_message_to_p_class_list_tuple(msg: dict, data_name: str, data_class: Any) -> Tuple[
    ErrorInfo, list]:
    error_info = ErrorInfo(msg['error_no'], msg['error_msg'])
    result_list = []
    data_items = msg['body'][data_name].get('data', None)
    fields = msg['body'][data_name].get('fields', None)
    if data_items is None or fields is None:
        return error_info, result_list
    for data_item in data_items:
        data_dict = dict(zip(fields, data_item))
        data_info = data_class(**data_dict)
        result_list.append(data_info)
    return error_info, result_list


def covert_message_to_dict_tuple(msg: dict, data_name: str):
    error_info = ErrorInfo(msg['error_no'], msg['error_msg'])
    result_list = {}
    if error_info.has_error():
        return error_info, result_list

    data_content = msg['body'].get(data_name, None)
    if data_content is None:
        return error_info, result_list
    data_item = msg['body'][data_name].get('data', None)
    fields = msg['body'][data_name].get('fields', None)
    if data_item is None or fields is None:
        return error_info, result_list
    result_list = dict(zip(fields, data_item))
    return error_info, result_list


def covert_message_to_class_list_tuple(msg: dict, data_name: str, data_class: Any, return_class: Any) -> Tuple[
    ErrorInfo, list]:
    error_info = ErrorInfo(msg['error_no'], msg['error_msg'])
    result_list = []

    data_info = msg['body'].get(data_name, None)
    if data_info is None:
        return error_info, result_list

    data_items = msg['body'][data_name].get('data', None)
    fields = msg['body'][data_name].get('fields', None)
    if data_items is None or fields is None:
        return error_info, result_list
    for data_item in data_items:
        data_dict = dict(zip(fields, data_item))
        data_info = data_class(**data_dict)
        result_list.append(return_class(data_info))
    return error_info, result_list


def covert_message_to_class_tuple(msg: dict, data_name: str, data_class: Any, return_class: Any) -> Tuple[
    ErrorInfo, Any]:
    error_info = ErrorInfo(msg['error_no'], msg['error_msg'])
    result_object = None
    data_info = msg['body'].get(data_name, None)
    if data_info is None:
        return error_info, result_object
    data_item = msg['body'][data_name].get('data', None)
    fields = msg['body'][data_name].get('fields', None)
    if data_item is None or len(data_item) == 0 or fields is None:
        return error_info, result_object

    data_dict = dict(zip(fields, data_item))
    data_info = data_class(**data_dict)
    return error_info, return_class(data_info)


def covert_message_to_order_class_tuple(msg: dict, data_name: str, data_class: Any, return_class: Any) -> Tuple[
    ErrorInfo, Any]:
    error_info = ErrorInfo(msg['error_no'], msg['error_msg'])
    result_object = None
    data_info = msg['body'].get(data_name, None)
    if data_info is None:
        return error_info, result_object
    data_item = msg['body'][data_name].get('data', None)
    fields = msg['body'][data_name].get('fields', None)
    if data_item is None or len(data_item) == 0 or fields is None:
        return error_info, result_object

    # data_item = data_items[0]
    data_dict = dict(zip(fields, data_item))
    data_info = data_class(**data_dict)
    return_object = return_class()
    return_object.set_value(data_info)
    return error_info, return_object


def covert_message_to_order_class_list_tuple(msg: dict, data_name: str, data_class: Any, return_class: Any) -> Tuple[
    ErrorInfo, Any]:
    error_info = ErrorInfo(msg['error_no'], msg['error_msg'])
    result_list = []
    data_info = msg['body'].get(data_name, None)
    if data_info is None:
        return error_info, result_list
    data_items = msg['body'][data_name].get('data', None)
    fields = msg['body'][data_name].get('fields', None)
    if data_items is None or len(data_items) == 0 or fields is None:
        return error_info, result_list
    for data_item in data_items:
        data_dict = dict(zip(fields, data_item))
        data_info = data_class(**data_dict)
        return_object = return_class()
        return_object.set_value(data_info)
        result_list.append(return_object)
    return error_info, result_list


"""
转换为主键为券的字典
"""


def covert_message_to_class_dict_tuple(msg: dict, data_name: str, data_class: Any, return_class: Any) -> Tuple[
    ErrorInfo, dict]:
    error_info = ErrorInfo(msg['error_no'], msg['error_msg'])
    result_dict = {}
    data_info = msg['body'].get(data_name, None)
    if data_info is None:
        return error_info, result_dict
    data_items = msg['body'][data_name].get('data', None)
    fields = msg['body'][data_name].get('fields', None)
    if data_items is None or fields is None:
        return error_info, result_dict
    for data_item in data_items:
        data_dict = dict(zip(fields, data_item))
        data_info = data_class(**data_dict)
        result_dict[data_info.security] = return_class(data_info)
    return error_info, result_dict


def covert_message_to_dataframe_tuple(msg: dict, data_name: str) -> Tuple[
    ErrorInfo, DataFrame]:
    error_info = ErrorInfo(msg['error_no'], msg['error_msg'])
    data_info = msg['body'].get(data_name, None)
    if data_info is None:
        return error_info, None
    data_items = msg['body'][data_name].get('data', None)
    fields = msg['body'][data_name].get('fields', None)
    if data_items is None or fields is None:
        return error_info, None
    df = pd.DataFrame(np.array(data_items), columns=fields)
    return error_info, df


def covert_csv_to_dataframe_tuple(msg: dict, converters: dict) -> Tuple[
    ErrorInfo, DataFrame]:
    error_info = ErrorInfo(msg['error_no'], msg['error_msg'])
    csv_bytes = msg.get('body', None)
    if csv_bytes is None or len(csv_bytes) == 0:
        return error_info, None
    csv_file_like = io.BytesIO(csv_bytes)
    df = pd.read_csv(csv_file_like, encoding='gbk', keep_default_na=False, converters=converters,sep="\t")
    return error_info, df
