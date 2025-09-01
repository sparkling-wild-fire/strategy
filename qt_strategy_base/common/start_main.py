# -*- coding: utf-8 -*-
import uuid
import xml
from xml.dom.minidom import parse
import datetime
import os
from qt_strategy_base.core.cache.global_params import GlobalParams


def start_main(strategy, params):
    from qt_strategy_base.core.common.local_log import local_logger
    if len(params) == 4:
        GlobalParams().ip_address = "127.0.0.1"
        GlobalParams().port = int(params[1])
        GlobalParams().strategy_id = params[2]
        process_uuid = params[3]

    else:
        process_uuid = str(uuid.uuid1())

    GlobalParams().strategy_name = strategy.__name__
    GlobalParams().strategy = strategy
    GlobalParams().process_uuid = process_uuid
    file_name = datetime.datetime.now().strftime(
        "%Y-%m-%d") + '-' + "python" + '-' + GlobalParams().strategy_id + '-' + GlobalParams().strategy_name + ".log"
    current_path = os.path.dirname(os.path.dirname(params[0]))
    config_file_path = os.path.join(current_path, "dlog_info.xml")
    log_level = read_log_level(path=config_file_path, strategy_id=GlobalParams().strategy_id)
    local_logger.init(logger_name="logger", file_name=file_name, path=current_path, logger_level=log_level)
    from qt_strategy_base.core.tcp_client import TcpClient
    TcpClient()


def set_base_info(ip_address, port, strategy_id,execute_mode):
    GlobalParams().ip_address = ip_address
    GlobalParams().port = port
    GlobalParams().strategy_id = strategy_id
    GlobalParams().execute_mode = execute_mode


def read_log_level(path, strategy_id) -> str:
    try:
        # 使用minidom解析器打开 XML 文档
        with open(path, 'rb') as f:
            file_xml = open(path, "r").read()
            file_xml = file_xml.replace('<?xml version="1.0" encoding="gbk"?>',
                                        '<?xml version="1.0" encoding="utf-8"?>')
            dom_tree = xml.dom.minidom.parseString(file_xml)
            collection = dom_tree.documentElement
            log_levels = collection.getElementsByTagName("log")
            for log_level in log_levels:
                if log_level.getAttribute("no") == strategy_id:
                    return log_level.getAttribute("def_level")
            return "1"
    except Exception as e:
        return "1"
