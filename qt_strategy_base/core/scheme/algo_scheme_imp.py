# -- coding: utf-8 --
from typing import Dict, List

from qt_strategy_base.core.cache.global_params import GlobalParams
from qt_strategy_base.core.model.model import PAlgoStrategy ,PAlgoDetail
from qt_strategy_base.core.scheme.algo_scheme_stock_impl import AlgoDetailImpl
from qt_strategy_base.model.algo_scheme import AlgoScheme
from qt_strategy_base.model.enum import Direction, Side, ControlType, SchemeType
from qt_strategy_base.model.error_info import ErrorInfo
from qt_strategy_base.model.strategy_api_data import AccountInfo


class AlgoSchemeImpl(AlgoScheme):

    def __init__(self, strategy_info: PAlgoStrategy, params_info: dict, strategy_params: dict,
                 control_type: ControlType):
        self._strategy_info: PAlgoStrategy = strategy_info
        self._params_info: dict = params_info
        self._strategy_params: dict = strategy_params
        self._control_type: ControlType = control_type
        self._algo_stock_detail_dict: Dict[str, AlgoDetailImpl] = {}
        self._algo_scheme_id: int = 0
        self._parent_scheme_id: int = 0
        self._scheme_status: SchemeType = SchemeType.UNINIT
        self._create_stock_detail:[AlgoDetailImpl]=[]

    def set_parent_scheme_id(self, parent_scheme_id: int):
        self._parent_scheme_id = parent_scheme_id

    def get_parent_scheme_id(self):
        return self._parent_scheme_id

    def get_algo_scheme_id(self):
        return self._algo_scheme_id

    def get_status(self) -> SchemeType:
        return self._scheme_status

    def set_status(self, scheme_status: SchemeType):
        self._scheme_status = scheme_status

    def update_params(self, new_params_dict: dict):
        for params_name, param_key in new_params_dict.items():
            self._strategy_params.update()
            if self._strategy_params.get(params_name, None) is not None:
                self._strategy_params[params_name] = param_key

    def get_param_info(self):
        """
        获取方案参数信息
        @return:
        """
        return self._params_info

    def set_param(self, param_name, value):
        """
        设置参数
        @param param_name: 参数名称
        @param value: 参数值
        @return:
        """
        error_info = ErrorInfo()
        param_type = self._params_info.get(param_name, None)
        if param_type is None:
            error_info.set_error_value(error_msg=f"{param_name}参数不存在！")
            return error_info
        param_type_error = False
        if param_type == "C":
            if not isinstance(value, str) or len(value) != 1:
                param_type_error = True
                error_info.set_error_value(error_msg=f"{param_name}参数数据类型有误！")
        elif param_type == "S":
            if not isinstance(value, str):
                param_type_error = True
                error_info.set_error_value(error_msg=f"{param_name}参数数据类型有误！")
        elif param_type == "I":
            if not isinstance(value, int):
                param_type_error = True
                error_info.set_error_value(error_msg=f"{param_name}参数数据类型有误！")
        elif param_type == "D":
            if not isinstance(value, float):
                param_type_error = True
                error_info.set_error_value(error_msg=f"{param_name}参数数据类型有误！")
        if param_type_error:
            return error_info
        else:
            self._strategy_params[param_name] = value
            return error_info

    def add_security_detail(self, security: str, account_info: AccountInfo, side: Side = None,
                            direction: Direction = None,
                            target_quantity: float = None,
                            target_value: float = None) -> ErrorInfo:
        """
        添加明细
        @param security:证券名称
        @param account_info:账户信息
        @param side:委托方向
        @param direction:开平仓方向
        @param target_quantity:目标数量
        @param target_value:目标金额
        @return:
        """


        error_info = ErrorInfo()
        if self._algo_scheme_id != 0:
            error_info.set_error_value(error_msg=f"方案已经创建，不能继续添加明细")
            return  error_info
        if self._control_type == ControlType.NO_CONTROL and (
                side is not None or direction is not None or target_quantity is not None or target_value is not None):
            error_info.set_error_value(error_msg=f"方案明细控制类别类型为不控制，请检查明细入参！")
            return error_info
        elif self._control_type == ControlType.VALUE_CONTROL and target_quantity is None:
            error_info.set_error_value(error_msg=f"方案明细控制类别类型按数量控制，请检查明细入参目标数量！")
            return error_info
        elif self._control_type == ControlType.QUANTITY_CONTROL and target_quantity is None:
            error_info.set_error_value(error_msg=f"方案明细控制类别类型按金额控制，请检查明细入参目标按金额！")
            return error_info
        security_arr = security.split('.')
        if len(security_arr) != 2:
            error_info.set_error_value(error_msg=f"security:{security}格式错误！")
            return error_info
        else:
            if security_arr[1] not in self._strategy_info.market_no_list:
                error_info.set_error_value(error_msg=f"security:{security}格式错误！")
                return error_info
        # if direction not in self._strategy_info.entrdirection_list:
        # error_info.set_error_value(error_msg=f"security:{direction}不符合方案要求！")
        # return error_info
        if target_quantity is None:
            target_quantity = 0
        if target_value is None:
            target_value = 0
        algo_detail = AlgoDetailImpl.gather_scheme_stocks_info(security=security, ctrl_type=self._control_type,
                                                               account_info=account_info, side=side,
                                                               direction=direction, target_quantity=target_quantity,
                                                               target_value=target_value)
        #self._algo_stock_detail_dict[algo_detail.third_remark] = algo_detail
        self._create_stock_detail.append(algo_detail)

        return error_info

    def get_all_details(self):
        return list(self._algo_stock_detail_dict.values())

    def run(self) -> ErrorInfo:
        """
        algo方案运行
        @return:错误信息
        """

        stock_fields: List[str] = ["security", "entrust_direction", "future_direction", "ins_price", "ins_balance",
                                   "ins_amount", "ctrl_type", "investunit_id", "instance_id", "invest_type"]

        stock_data: List[list] = []
        current_scheme_id = GlobalParams().current_scheme_id
        algo_strategy_param = ""
        for param_name, param_value in self._strategy_params.items():
            algo_strategy_param = algo_strategy_param + f"<{param_name}>{param_value}</{param_name}>"

        for algo_detail in self._create_stock_detail:
            side = 0 if algo_detail.side is None else algo_detail.side.value
            direction = 0 if algo_detail.direction is None else algo_detail.direction.value

            data_item = [algo_detail.security, side, direction, 0, algo_detail.target_value,
                         algo_detail.target_quantity, algo_detail.control_type.value,
                         algo_detail.get_account().investunit_id, algo_detail.get_account().portfolio_id,
                         algo_detail.get_account().invest_type.value, current_scheme_id,
                         self._strategy_info.strategy_id, "", algo_strategy_param]
            stock_data.append(data_item)

        scheme_fields: List[str] = ["create_scheme_id", "strategy_id", "scheme_name", "algo_strategy_param"]
        scheme_data: List[list] = [current_scheme_id, self._strategy_info.strategy_id, "", algo_strategy_param]
        scheme_stocks = {"fields": stock_fields, "data": stock_data}
        scheme_info = {"fields": scheme_fields, "data": scheme_data}
        request_params = {"body": {"scheme_stocks": scheme_stocks, "scheme_info": scheme_info}}

        from qt_strategy_base.core.common.aglo_function_impl import FunctionImpl
        error_info, scheme_dict = FunctionImpl.run_algo_scheme(request_params=request_params)
        algo_scheme_id = scheme_dict.get("scheme_id", None)
        if algo_scheme_id is not None:
            self._algo_scheme_id = algo_scheme_id

            from qt_strategy_base.core.cache.sub_scheme_manage import SubSchemeManager
            sub_scheme_manager: SubSchemeManager = SubSchemeManager()
            sub_scheme_manager.add_scheme(algo_scheme=self)
        return error_info

    def cancel(self) -> ErrorInfo:
        """
        algo方案撤销
        @return:错误信息
        """
        error_info = ErrorInfo()
        if self._algo_scheme_id == 0:
            error_info.set_error_value("方案号为0！")
        else:
            from qt_strategy_base.core.common.aglo_function_impl import FunctionImpl
            error_info, scheme_dict = FunctionImpl.cancel_algo_scheme(self._algo_scheme_id)
        return error_info
    def update_detail(self,detail_info:PAlgoDetail)  -> AlgoDetailImpl:
        algo_detail :AlgoDetailImpl = self._algo_stock_detail_dict.get(detail_info.id,None)
        if algo_detail is None:
            algo_detail :AlgoDetailImpl  = AlgoDetailImpl.gather_scheme_stocks_info(security=detail_info.security , ctrl_type=self._control_type, side=detail_info.side,
                                                                   direction=detail_info.direction, target_quantity=detail_info.target_quantity,
                                                                   target_value=detail_info.target_value,account_info=None)

            algo_detail.update_value(detail_info)
            self._algo_stock_detail_dict[algo_detail.id] = algo_detail
            return algo_detail
        else:
            algo_detail.update_value(detail_info)
            return algo_detail

