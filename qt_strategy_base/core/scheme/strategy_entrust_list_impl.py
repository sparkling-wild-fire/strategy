# -*- coding: utf-8 -*-
from qt_strategy_base.core.common.public_func import get_order_id
from qt_strategy_base.core.scheme.strategy_order_impl import OrderData, OrderDataImpl
from qt_strategy_base.model.enum import CloseType, Side, Direction, OrderStatus


class CAlgoEntrustListImpl(object):

    def __init__(self, scheme):

        self._scheme = scheme
        self._all_order_dict_by_internal_id = {}
        self._open_order_dict_by_internal_id = {}

    def create_limit_entrust(self, price: float, quantity: float, side: Side,
                             direction: Direction, close_type: CloseType,
                             scheme_ins_code: str, remark: str,security:str) -> OrderData:
        """
        生成限价委托
        @param price: 价格
        @param quantity: 数量
        @param side: 委托方向
        @param direction: 开平方向
        @param close_type: 开平类型
        @param scheme_ins_code: 明细id
        @param remark: 备注
        @param security:证券代码
        @return:
        """
        entrust_info = OrderDataImpl()
        entrust_info.set_security(security)
        entrust_info.set_scheme_id(self._scheme.scheme_id)
        entrust_info.set_internal_id(get_order_id())
        entrust_info.set_security_detail_id(scheme_ins_code)
        entrust_info.set_price(price)
        entrust_info.set_quantity(quantity)
        entrust_info.set_close_type(close_type)
        entrust_info.set_remark(remark)
        entrust_info.set_side(side)
        entrust_info.set_direction(direction)
        entrust_info.set_status(OrderStatus.UNREPORT)
        self.insert_entrust(entrust_info)
        return entrust_info

    def recover_entrust(self, entrust_info: OrderData):
        """
        恢复委托
        @param entrust_info:
        """
        self.insert_entrust(entrust_info=entrust_info)

    def insert_entrust(self, entrust_info: OrderData):
        """
        插入order_id字典中
        :param entrust_info:委托数据信息
        :return:
        """
        self._open_order_dict_by_internal_id[entrust_info.internal_id] = entrust_info
        self._all_order_dict_by_internal_id[entrust_info.internal_id] = entrust_info

    def del_entrust(self, entrust: OrderData):
        """
        从order_id字典中删除
        :param entrust:委托数据信息
        :return:
        """
        if entrust.internal_id in self._all_order_dict_by_internal_id.keys():
            del self._all_order_dict_by_internal_id[entrust.internal_id]

    def _if_keep_final_state_entrust(self) -> bool:
        """
        判断是否保留终态委托
        :return:True 保留，否则不保留
        """
        return self._scheme.keep_final_state_entrust

    # 仅查询返回委托记录
    def on_entrust_req_accept(self, order_id: str) -> OrderData:
        """
        单纯的查询委托是否在order_id字典中
        :param order_id:子单号
        :return:OrderDataImpl
        """
        return self.find_entrust(order_id)

    def find_entrust(self, order_id: str) -> OrderData:
        """
        从字典中找委托记录
        :param order_id:子单号
        :return:OrderDataImpl,找不到返回默认None
        """
        return self._all_order_dict_by_internal_id.get(order_id, None)

    def _find_if_del_entrust(self, order_id: str) -> OrderData:
        """
        查找流水缓存 如果不需要保持终态 就删除
        :param order_id:子单号
        :return:OrderDataImpl
        """
        ret = self.find_entrust(order_id)
        if ret is not None and not self._if_keep_final_state_entrust():
            self.del_entrust(ret)
        if ret.internal_id in self._open_order_dict_by_internal_id.keys():
            del self._open_order_dict_by_internal_id[ret.internal_id]
        return ret

    def get_iterator(self, scheme_ins_code: str = ""):
        """
        返回方案明细的迭代列表
        :param scheme_ins_code:方案明细序代码
        :return:
        """
        if scheme_ins_code == "":
            for entrust in self._all_order_dict_by_internal_id.values():
                yield entrust
        else:
            for entrust in self._all_order_dict_by_internal_id.values():
                if entrust.security_detail_id == scheme_ins_code:
                    yield entrust

    def get_entrust_list(self):
        return self._all_order_dict_by_internal_id.values()

    def update_un_final_state_entrust(self, new_order_data: OrderData):
        ret = self.find_entrust(new_order_data.internal_id)
        if ret is not None:
            self._all_order_dict_by_internal_id[new_order_data.internal_id] = new_order_data
            self._open_order_dict_by_internal_id[new_order_data.internal_id] = new_order_data
            return new_order_data
        else:
            return None

    def update_final_state_entrust(self, new_order_data: OrderData):
        self._find_if_del_entrust(new_order_data.internal_id)
        return new_order_data

    def get_open_order(self):
        return self._open_order_dict_by_internal_id.values()
