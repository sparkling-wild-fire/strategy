# -*- coding: utf-8 -*-
import concurrent
import datetime
import json
import os
import struct
import threading
import time
import socket
import traceback
import uuid

from qt_strategy_base.model.enum import ExecuteMode
from qt_strategy_base.core.cache.global_params import GlobalParams
from qt_strategy_base.core.common.local_log import local_logger
from qt_strategy_base.core.common.public_func import kill_current_process, msg_package_covert
from qt_strategy_base.core.common.constant import FunctionID
from qt_strategy_base.core.cache.id_manage import PackageIdManager
from qt_strategy_base.core.scheme.callback_message_handle import CallbackMessageHandler
from threading import Thread
from typing import List
from qt_strategy_base.common.singleton import singleton
from qt_strategy_base.core.scheme.message_distribute import MessageDistribute
from qt_strategy_base.model.error_info import ErrorInfo


@singleton
class TcpClient:
    def __init__(self):

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._global_params: GlobalParams = GlobalParams()
        self._port = self._global_params.port
        self._id_address = self._global_params.ip_address
        self._mac = self.get_mac_address()
        self._start_bytes = b'\xef\xef\xef\xef'
        self._end_bytes = b'\xfe\xfe\xfe\xfe'
        self._check_bytes = b'\x00\x00\x00\x00'
        self._incomplete_message_bytes = b''
        # tcp连接参数，先判断是否能连接
        try:
            self._sock.connect((self._id_address, self._port))
        except Exception as e:
            raise ConnectionError("无法建立连接!")
        self.recv_buffer_size = 10 * 1024 * 1024
        local_logger.info("tcp连接成功")

        # 同步应答消息集合
        self._answer_dict = {}
        self._callback_message_handler_num = 1
        self._request_package_id = 0
        self._callback_message_handler = CallbackMessageHandler()
        self.send_login_mess()
        self._message_distribute = MessageDistribute(self._callback_message_handler)
        self._message_accept_thread = Thread(target=self.message_accept)
        self._message_accept_thread.start()

        self._maintain_thread = Thread(target=self.maintain_heartbeat)
        self._maintain_thread.start()

    def params_to_bytes(self, function_id: int, package_id: int, scheme_id: int, request_params: dict):
        bytes_function_id = function_id.to_bytes(4, byteorder='little')
        bytes_scheme_id = scheme_id.to_bytes(4, byteorder='little')
        bytes_package_id = package_id.to_bytes(4, byteorder='little')
        package_data = json.dumps(request_params).encode(encoding='utf-8', errors='strict')
        package_data_len = len(package_data)
        bytes_package_data_len = package_data_len.to_bytes(4, byteorder='little')

        bytes_package_type = b'1'
        bytes_compression_type = b'1'
        current_timestamp = datetime.datetime.now().timestamp()

        bytes_current_timestamp = struct.pack('d', current_timestamp)

        request_content = self._start_bytes + bytes_function_id + bytes_scheme_id + bytes_package_id + bytes_package_data_len + bytes_package_type + bytes_compression_type + bytes_current_timestamp + package_data + self._check_bytes + self._end_bytes

        return request_content

    def get_mac_address(self):
        """
        获取本机物理地址，获取本机mac地址
        :return:
        """
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:].upper()
        return "-".join([mac[e:e + 2] for e in range(0, 11, 2)])

    def maintain_heartbeat(self):
        while True:
            from qt_strategy_base.core.cache.scheme_manage import SchemeManage
            scheme_num = SchemeManage().get_scheme_num()

            total_req_num = self._callback_message_handler.get_message_num()
            fields: List[str] = ["mac", "scheme_num", "req_num", "strategy_no", "process_uuid"]
            data: List[list] = [
                [self._mac, scheme_num, total_req_num, GlobalParams().strategy_id, GlobalParams().process_uuid]]
            self.make_request_no_recv(scheme_id=0, function_id=FunctionID.SendTcpStatus.value, fields=fields,
                                      data=data)
            time.sleep(1)

    def find_relaxed_async_handle_thread(self) -> CallbackMessageHandler:
        self._callback_message_handler.check_thread_status()
        return self._callback_message_handler

    def construct_params(self, fields: list, data: list) -> dict:
        base_params = {"body": {"fields": [], "data": []}}
        base_params['body']['fields'] = fields
        base_params['body']['data'] = data
        return base_params

    # 接受所有的消息，对于多个包进行拆包操作
    def message_accept(self):
        while True:
            try:
                message_bytes = self._sock.recv(self.recv_buffer_size)
                #print(message_bytes)
                if len(message_bytes) == 0:
                    kill_current_process()
                if len(self._incomplete_message_bytes) != 0:
                    message_bytes = self._incomplete_message_bytes + message_bytes
                    self._incomplete_message_bytes = b''
                start_index = 0
                message_len = len(message_bytes)
                while True:
                    one_message_start_index = message_bytes.find(self._start_bytes, start_index)

                    if one_message_start_index == -1:
                        break
                    one_package_head_start = one_message_start_index + 4
                    one_package_head_end = one_message_start_index + 30
                    if one_message_start_index > message_len or one_package_head_end > message_len:
                        self._incomplete_message_bytes = self._incomplete_message_bytes + message_bytes[
                                                                                          one_message_start_index:message_len]
                        local_logger.info(f"消息包不完整！{self._incomplete_message_bytes}")
                        break


                    function_id = struct.unpack("i", message_bytes[one_package_head_start: one_package_head_start + 4])[
                        0]
                    scheme_id = \
                        struct.unpack("i", message_bytes[one_package_head_start + 4: one_package_head_start + 8])[0]
                    package_id = \
                        struct.unpack("i", message_bytes[one_package_head_start + 8: one_package_head_start + 12])[0]
                    package_data_len = \
                        struct.unpack("i", message_bytes[one_package_head_start + 12: one_package_head_start + 16])[0]
                    pack_type = \
                        struct.unpack("c", message_bytes[one_package_head_start + 16: one_package_head_start + 17])[
                            0].decode()
                    compression_type = \
                        struct.unpack("c", message_bytes[one_package_head_start + 17: one_package_head_start + 18])[
                            0].decode()
                    timestamp = \
                        struct.unpack("d", message_bytes[one_package_head_start + 18: one_package_head_start + 26])[0]
                    one_package_body_start = one_message_start_index + 30
                    one_package_body_end = one_message_start_index + 30 + package_data_len
                    if one_message_start_index > message_len or one_package_body_end > message_len:
                        self._incomplete_message_bytes = self._incomplete_message_bytes + message_bytes[
                                                                                          one_message_start_index:message_len]
                        local_logger.info(f"消息包不完整！{self._incomplete_message_bytes}")
                        break
                    one_message_content = message_bytes[one_package_body_start:one_package_body_end]

                    local_logger.info(
                        f"function_id:{function_id},package_id:{package_id},scheme_id:{scheme_id},package_data_len:{package_data_len},timestamp:{timestamp},compression_type:{compression_type},pack_type:{pack_type}")

                    local_logger.debug(f"message_content:{one_message_content}")

                    start_index = one_package_body_end  # 从下一个位置开始查找

                    msg_dict = {"function_id": function_id, "package_id": package_id, "scheme_id": scheme_id,
                                "timestamp": timestamp, "compression_type": compression_type, "pack_type": pack_type,
                                "package_data_len": package_data_len, "msg_content": one_message_content}
                    self.message_handle(msg_dict)

            except Exception as ex:
                local_logger.error("message_accept异常：" + str(ex))
                local_logger.error(traceback.format_exc())
                kill_current_process()
                raise ex
        pass

    def message_handle(self, msg_dict: dict):
        from qt_strategy_base.core.scheme.fuction_collection import FUNCTION_INFO_DICT, FunctionType, FunctionInfo
        function_id = msg_dict.get('function_id', 0)
        package_id = msg_dict.get('package_id', 0)
        scheme_id = msg_dict.get('scheme_id', 0)
        function_info: FunctionInfo = FUNCTION_INFO_DICT.get(function_id, None)
        if function_info is None:
            local_logger.error(f"function_info：{function_id}不存在")
            return
        # 创建方案消息处理
        if function_info.function_type == FunctionType.CREATE.value:
            self._message_distribute.create_message_handle(scheme_id, msg_dict)
        # 注销方案消息处理
        elif function_info.function_type == FunctionType.STOP.value:
            self._message_distribute.stop_message_handle(scheme_id)
        # 回调消息处理
        elif function_info.function_type == FunctionType.CALLBACK.value:
            self._message_distribute.callback_message_handle(msg_dict)
        # 批量回调消息处理，一个消息触发多个方案回调函数，例如行情
        elif function_info.function_type == FunctionType.BatchCALLBACK.value:
            self._message_distribute.callback_message_handle(msg_dict)
        # 查询消息处理
        elif function_info.function_type == FunctionType.QUERY.value:
            if package_id == self._request_package_id:
                self._answer_dict[package_id] = msg_dict
                self._request_package_id = -1
                self._callback_message_handler.thread_resume()
        else:
            pass

    # 发出请求，不需要等消息应答
    def make_request_no_recv(self, scheme_id: int, function_id: int, fields: list, data: list):
        try:
            if scheme_id == 0 and threading.get_ident() == self._callback_message_handler.get_thread_id():
                scheme_id = self._global_params.current_scheme_id
            package_id = PackageIdManager().get_package_id()
            request_params = self.construct_params(fields=fields, data=data)
            request_params_str = self.params_to_bytes(function_id=function_id, package_id=package_id,
                                                      scheme_id=scheme_id,
                                                      request_params=request_params)
            # print(request_params_str)
            self._sock.send(request_params_str)

        except ConnectionError as e:
            local_logger.error(str(e))
            kill_current_process()
        except Exception as e:
            local_logger.error(str(e))

    # 发出请求，需要等消息应答
    def make_request(self, scheme_id: int, function_id: int, fields: list, data: list):
        error_info = ErrorInfo()
        if scheme_id == 0 and threading.get_ident() == self._callback_message_handler.get_thread_id():
            scheme_id = self._global_params.current_scheme_id
        package_id: int = PackageIdManager().get_package_id()

        request_params: dict = self.construct_params(fields=fields, data=data)
        request_params_str: bytes = self.params_to_bytes(function_id=function_id, package_id=package_id,
                                                         scheme_id=scheme_id,
                                                         request_params=request_params)

        local_logger.info(f"同步接口正在等待...,功能号：{function_id},请求内容：{request_params}")
        self._request_package_id = package_id
        try:
            self._sock.sendall(request_params_str)
            if self._request_package_id != -1:  # 处理消息返回太快还没有开始等待就已经返回的情况
                self._callback_message_handler.thread_wait(60)
        except ConnectionError as e:
            local_logger.error(str(e))
            kill_current_process()

        # 同步等待消息回来,判断传入的id和接受的id是否一致
        if not len(self._answer_dict) == 0 and package_id in self._answer_dict.keys():
            # 如果一致，则将包转成特定的格式，释放锁，再返回结果
            result = self._answer_dict[package_id]
            del self._answer_dict[package_id]
            local_logger.info(f"同步接查询成功,功能号：{function_id}")
            pack_type: int = result.get("pack_type", None)
            msg_content: str = result.get("msg_content", None)
            if msg_content is None or pack_type is None:
                result = {"function_id": function_id, "package_id": package_id, "scheme_id": scheme_id,
                          "timestamp": "", "compression_type": "", "pack_type": "0", "package_data_len": 0,
                          "msg_content": {"error_no": -1,
                                          "error_msg": f"同步接口返回数据格式错误,功能号：{function_id}，package_id：{package_id}",
                                          "body": {}}}
                local_logger.info(f"同步接口返回数据格式错误,功能号：{function_id}，package_id：{package_id}")
            else:
                msg_package_covert(result)

            return result['msg_content']
        else:
            result = {"function_id": function_id, "package_id": package_id, "scheme_id": scheme_id,
                      "timestamp": "", "compression_type": "", "pack_type": "0", "package_data_len": 0,
                      "msg_content": {"error_no": -1, "error_msg": f"同步接口调用超时,功能号：{function_id}",
                                      "body": {}}}
            local_logger.info(f"同步接口调用超时,功能号：{function_id}，超时时间：60s")
            return result['msg_content']

    # 发出请求，需要等消息应答，多消息包时使用
    def make_request2(self, scheme_id: int, function_id: int, request_params: dict):
        error_info = ErrorInfo()
        if scheme_id == 0 and threading.get_ident() == self._callback_message_handler.get_thread_id():
            scheme_id = self._global_params.current_scheme_id
        package_id: int = PackageIdManager().get_package_id()
        request_params_str: bytes = self.params_to_bytes(function_id=function_id, package_id=package_id,
                                                         scheme_id=scheme_id,
                                                         request_params=request_params)

        local_logger.info(f"同步接口正在等待...,功能号：{function_id},请求内容：{request_params}")
        self._request_package_id = package_id
        try:
            self._sock.sendall(request_params_str)
            if self._request_package_id != -1:  # 处理消息返回太快还没有开始等待就已经返回的情况
                self._callback_message_handler.thread_wait(60)
        except ConnectionError as e:
            local_logger.error(str(e))
            kill_current_process()

        # 同步等待消息回来,判断传入的id和接受的id是否一致
        if not len(self._answer_dict) == 0 and package_id in self._answer_dict.keys():
            # 如果一致，则将包转成特定的格式，释放锁，再返回结果
            result = self._answer_dict[package_id]
            del self._answer_dict[package_id]
            local_logger.info(f"同步接查询成功,功能号：{function_id}")
            pack_type: int = result.get("pack_type", None)
            msg_content: str = result.get("msg_content", None)
            if msg_content is None or pack_type is None:
                result = {"function_id": function_id, "package_id": package_id, "scheme_id": scheme_id,
                          "timestamp": "", "compression_type": "", "pack_type": "0", "package_data_len": 0,
                          "msg_content": {"error_no": -1,
                                          "error_msg": f"同步接口返回数据格式错误,功能号：{function_id}，package_id：{package_id}",
                                          "body": {}}}
                local_logger.info(f"同步接口返回数据格式错误,功能号：{function_id}，package_id：{package_id}")
            else:
                msg_package_covert(result)

            return result['msg_content']
        else:
            result = {"function_id": function_id, "package_id": package_id, "scheme_id": scheme_id,
                      "timestamp": "", "compression_type": "", "pack_type": "0", "package_data_len": 0,
                      "msg_content": {"error_no": -1, "error_msg": f"同步接口调用超时,功能号：{function_id}",
                                      "body": {}}}
            local_logger.info(f"同步接口调用超时,功能号：{function_id}，超时时间：60s")
            return result['msg_content']

    # 发出应答
    def make_response_no_recv(self, scheme_id: int, package_id: int, function_id: int, fields: list, data: list):
        try:
            request_params = self.construct_params(fields=fields, data=data)
            request_params_str = self.params_to_bytes(function_id=function_id, package_id=package_id,
                                                      scheme_id=scheme_id,
                                                      request_params=request_params)

            self._sock.send(request_params_str)
        except ConnectionError as e:
            local_logger.error(str(e))
            kill_current_process()
        except Exception as e:
            local_logger.error(str(e))

    def dispose(self):
        self._sock.close()
        pass

    def send_login_mess(self):
        fields: List[str] = ["uuid", "remote_flag"]
        uuid_str = GlobalParams().process_uuid
        data: List[str] = [[uuid_str, GlobalParams().execute_mode.value]]
        self.make_request_no_recv(scheme_id=0, function_id=FunctionID.Login.value, fields=fields,
                                  data=data)
