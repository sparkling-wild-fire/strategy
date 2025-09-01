# -- coding: utf-8 --
import threading
from typing import Tuple, List, Dict

from qt_strategy_base.core.common.public_func import covert_to_enum
from qt_strategy_base.core.cache.global_params import GlobalParams
from qt_strategy_base.core.model.model import PAlgoScheme
from qt_strategy_base.core.scheme.algo_scheme_imp import AlgoSchemeImpl
from qt_strategy_base.model.algo_detail import AlgoDetail
from qt_strategy_base.model.error_info import ErrorInfo
from qt_strategy_base.core.common.aglo_function_impl import FunctionImpl
from qt_strategy_base.model.enum import ControlType,SchemeType,SecurityDetailStatus
from qt_strategy_base.common.singleton import singleton
from qt_strategy_base.core.scheme.callback_message_handle import CallbackMessageHandler
from qt_strategy_base.model.algo_scheme import AlgoScheme


@singleton
class SubSchemeManager:
    def __init__(self):
        self._sub_scheme_manage_dict: Dict[int, List[AlgoSchemeImpl]] = {}  # 键为父方案id，值为子方案列表
        self._all_sub_scheme_dict: Dict[int, AlgoSchemeImpl] = {}  # 键为子方案id，值为子方案
        self._global_params = GlobalParams()
        self._callback_message_handler = CallbackMessageHandler()

    def create_scheme(self, strategy_id: int, control_type: ControlType) -> Tuple[ErrorInfo, AlgoScheme]:
        create_info = ErrorInfo()
        scheme_id = 0
        if threading.get_ident() == self._callback_message_handler.get_thread_id():
            scheme_id = self._global_params.current_scheme_id
        else:
            create_info.set_error_value("创建方案使用的线程错误，创建失败！")
            return create_info, None

        create_info, sub_scheme = FunctionImpl.get_sub_scheme(strategy_id=strategy_id, control_type=control_type)
        if not create_info.has_error():
            sub_scheme.set_parent_scheme_id(parent_scheme_id=scheme_id)
        return create_info, sub_scheme

    def add_scheme(self, algo_scheme: AlgoSchemeImpl):
        parent_scheme_id = algo_scheme.get_parent_scheme_id()
        algo_scheme_id = algo_scheme.get_algo_scheme_id()
        self._all_sub_scheme_dict[algo_scheme_id] = algo_scheme
        if self._sub_scheme_manage_dict.get(parent_scheme_id, None) is None:
            self._sub_scheme_manage_dict[parent_scheme_id] = [algo_scheme]
        else:
            self._sub_scheme_manage_dict[parent_scheme_id].append(algo_scheme)

    def update_scheme(self, p_algo_scheme: PAlgoScheme):
        algo_scheme = self._all_sub_scheme_dict.get(p_algo_scheme.scheme_id, None)
        if algo_scheme is not None:
            algo_scheme.set_status(covert_to_enum(p_algo_scheme.scheme_status,SchemeType))
            #param_dict = {}  # Todo
            #algo_scheme.update_params(new_params_dict=param_dict)

    def get_security_details(self) -> List[AlgoDetail]:
        security_details_list = []
        if threading.get_ident() == self._callback_message_handler.get_thread_id():
            scheme_id = self._global_params.current_scheme_id
            algo_scheme_list = self._sub_scheme_manage_dict.get(scheme_id, [])
            for algo_scheme in algo_scheme_list:
                security_details_list = security_details_list + algo_scheme.get_all_details()
            return security_details_list
        else:
            return security_details_list

    def get_all_scheme(self) -> List[AlgoScheme]:
        scheme_id = self._global_params.current_scheme_id
        if scheme_id != 0:
            sub_scheme_list: List[int] = self._sub_scheme_manage_dict.get(scheme_id, [])
            return sub_scheme_list
        else:
            return []

    def get_scheme(self, scheme_id):
        algo_scheme = self._all_sub_scheme_dict.get(scheme_id, None)
        return algo_scheme
