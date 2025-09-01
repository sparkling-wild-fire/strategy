# -*- coding: utf-8 -*-
import datetime
import json
import struct
import time
from enum import Enum
import  base64
import  pickle

import pandas as pd

from qt_strategy_base.core.common import python_logger
from qt_strategy_base.core.common.local_log import local_logger

__ymd_format = "%Y%m%d"
__ymdHMS_format = "%Y%m%d%H%M%S"


def get_mill() -> int:
    mil_sec = int(round(time.time() * 1000_000))  # 获取微妙级的时间戳
    return mil_sec


def fix_date_time_to_dt(fix_date_time: str) -> int:
    try:
        # c++ FixDateTimeToDT
        s_fix = fix_date_time
        found = s_fix.find('-')
        if found != -1:
            s_fix = s_fix.replace('-', '', 1)
        s_fix = s_fix.replace(':', '')
        t = datetime.datetime.strptime(str(s_fix), __ymdHMS_format)
        out_day = (t + datetime.timedelta(hours=8)).strftime(__ymdHMS_format)
        return int(out_day)
    except ValueError as e:
        python_logger.error(f"{fix_date_time}不是正确的日期格式")
        return int(fix_date_time)


def date_add(day: int, increment: int) -> int:
    # c++ hs_dateadd
    t = datetime.datetime.strptime(str(day), __ymd_format)
    out_day = (t + datetime.timedelta(days=increment)).strftime(__ymd_format)
    return int(out_day)


def get_cur_date() -> int:
    ts = time.localtime()
    t_date = ts.tm_year * 10000 + ts.tm_mon * 100 + ts.tm_mday
    t_time = t_date * 1000000 + ts.tm_hour * 10000 + ts.tm_min * 100 + ts.tm_sec
    return t_time


def get_short_date() -> int:
    ts = time.localtime()
    t_date = ts.tm_year * 10000 + ts.tm_mon * 100 + ts.tm_mday
    return t_date


def int_time_to_str(timestamp: int) -> str:
    hours = timestamp // 10000000
    minutes = (timestamp % 10000000) // 100000
    seconds = (timestamp % 100000) // 1000
    milliseconds = timestamp % 1000

    # 使用字符串格式化来组合时间
    time_str = "{:02d}:{:02d}:{:02d}.{:03d}".format(hours, minutes, seconds, milliseconds)

    return time_str


def diffdatetime_tosec(time1: int, time2: int) -> int:
    dt1 = datetime.datetime.strptime(str(time1), __ymdHMS_format)
    dt2 = datetime.datetime.strptime(str(time2), __ymdHMS_format)
    diff = 0
    if dt2 > dt1:
        diff = (dt2 - dt1).seconds
    else:
        diff = (dt1 - dt2).seconds
    return diff


def get_time_now() -> int:
    ts = time.localtime()
    t_time = ts.tm_hour * 10000 + ts.tm_min * 100 + ts.tm_sec
    return t_time


def covert_to_enum(enum_value, enum_class: Enum):
    if enum_value in enum_class._value2member_map_:
        return enum_class(enum_value)
    else:
        return None


def get_order_id() -> str:
    from qt_strategy_base.core.common.aglo_function_impl import FunctionImpl
    from qt_strategy_base.core.common import python_logger
    from qt_strategy_base.core.cache.id_manage import OrderIdManager
    status, order_id = OrderIdManager().get_order_id()
    if not status:
        error_info, data_dict_list = FunctionImpl.get_section_no()
        if error_info.has_error():
            python_logger.error("获取section_no失败")
        else:
            python_logger.info("获取section_no成功")
            section_no = data_dict_list['section_no']
            order_id = OrderIdManager().update_order_id_start(section_no)
    return order_id


def kill_current_process():
    import os
    import signal
    import sys
    if "linux" in sys.platform:
        local_logger.info(f"linux下,{os.getpid()}进程将被杀掉")
        os.kill(os.getpid(), signal.SIGKILL)
    else:
        local_logger.info(f"{os.getpid()}进程将被杀掉")
        os.system('taskkill /f /pid %s' % os.getpid())


def covert_order_data_to_dataframe(order_list):
    data_list = []
    for item in order_list:
        order_item = [item.id, item.security, item.datetime, item.price, item.quantity, item.side, item.direction,
                      item.close_type, item.status, item.invest_type, item.internal_id, item.revoke_cause,
                      item.cancel_quantity, item.investunit_id, item.portfolio_id, item.filled_quantity,
                      item.filled_value, item.remark, item.scheme_id, item.security_detail_id, item.operator_no]
        data_list.append(order_item)
    return pd.DataFrame(data_list,
                        columns=['id', 'security', 'datetime', 'price', 'quantity', 'side',
                                 'direction', 'close_type', 'status',
                                 'invest_type', 'internal_id', 'revoke_cause',
                                 'cancel_quantity', 'investunit_id', 'portfolio_id', 'filled_quantity',
                                 'filled_value', 'remark', 'scheme_id', 'security_detail_id', 'operator_no'])


def msg_package_covert(msg: dict):
    msg_content = msg.get("msg_content", None)
    package_data_len = msg.get("package_data_len", None)
    package_type = msg.get("pack_type", None)
    if msg_content is None or package_data_len is None or package_type is None:
        return
    if package_type == "1":
        msg_content = msg_content.decode('gbk', 'ignore')
        msg['msg_content'] = json.loads(msg_content)
    elif package_type == "2":
        package_start = 0
        error_no = struct.unpack("i", msg_content[package_start: package_start + 4])[0]
        error_msg_len = struct.unpack("i", msg_content[package_start + 4: package_start + 8])[0]
        error_msg = msg_content[package_start + 8: package_start + 8 + error_msg_len].decode('gbk', 'ignore')
        csv_bytes = msg_content[package_start + 8: package_start + package_data_len - error_msg_len]
        msg['msg_content'] = {'error_no': error_no, 'error_msg': error_msg, 'body': csv_bytes}


def object_to_base64(obj):
    # 第一步：将对象序列化为字节流
    serialized_obj = pickle.dumps(obj)
    # 第二步：进行 Base64 编码
    encoded = base64.b64encode(serialized_obj)
    # 第三步：将 bytes 转换为字符串
    return encoded.decode('utf-8')


def base64_to_object(b64_str):
    # 第一步：将字符串转回 bytes
    encoded = b64_str.encode('utf-8')
    # 第二步：解码 Base64
    serialized_obj = base64.b64decode(encoded)
    # 第三步：反序列化为原始对象
    return pickle.loads(serialized_obj)
