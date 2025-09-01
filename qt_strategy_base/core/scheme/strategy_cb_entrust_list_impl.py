# -*- coding: utf-8 -*-
from qt_strategy_base import PushType, OrderStatus
from qt_strategy_base.core.common import python_logger
from qt_strategy_base.core.model.model import PCombOrderData
from qt_strategy_base.core.scheme.strategy_cb_order_impl import CombOrderDataImpl
from qt_strategy_base.model.comb_order import CombOrderData


class CAlgoCBEntrustListImpl(object):

    def __init__(self, scheme):

        self._scheme = scheme
        self._final_order_id = set()
        self._cb_entrust_info_dict = {}  # 主键为algo_order_id
        self._cb_entrust_no_info_dict = {}  # 主键为合笔委托号
        self._entrust_no_info_dict = {}  # 主键为单笔委托号
        self._scheme_canceling = False

    def insert_entrust(self, entrust_info: CombOrderDataImpl):
        """
        插入order_id字典中
        :param entrust_info:委托数据信息
        :return:
        """
        if entrust_info.internal_id in self._final_order_id:
            return
        self._cb_entrust_info_dict[entrust_info.internal_id] = entrust_info
        if entrust_info.id > 0:
            self._cb_entrust_no_info_dict[entrust_info.id] = entrust_info

        if entrust_info.buy_id > 0:
            self._entrust_no_info_dict[entrust_info.buy_id] = entrust_info

        if entrust_info.sell_id > 0:
            self._entrust_no_info_dict[entrust_info.sell_id] = entrust_info

        python_logger.debug(f"方案:{entrust_info.scheme_id}将子单信息加入管理，子单号：{entrust_info.internal_id}")

    def del_entrust(self, internal_id: str):
        cb_entrust_info: CombOrderDataImpl = self._cb_entrust_info_dict.get(internal_id, None)
        if cb_entrust_info is not None:
            python_logger.info(f"方案删除{self._scheme.scheme_id}终态{internal_id}子单")
            if cb_entrust_info.id > 0 and cb_entrust_info.id in self._cb_entrust_no_info_dict.keys():
                del self._cb_entrust_no_info_dict[cb_entrust_info.id]
            if cb_entrust_info.buy_id > 0 and cb_entrust_info.buy_id in self._entrust_no_info_dict.keys():
                del self._entrust_no_info_dict[cb_entrust_info.buy_id]
            if cb_entrust_info.sell_id > 0 and cb_entrust_info.sell_id in self._entrust_no_info_dict.keys():
                del self._entrust_no_info_dict[cb_entrust_info.sell_id]
            del self._cb_entrust_info_dict[internal_id]
            self._final_order_id.add(internal_id)

    def entrust_reject(self, internal_id: str, revoke_cause: str, id: int = 0, buy_id: int = 0, sell_id: int = 0):
        cb_entrust_info: CombOrderDataImpl = self._cb_entrust_info_dict.get(internal_id, None)
        if cb_entrust_info is not None:
            cb_entrust_info.update_comb_entrust(revoke_cause=revoke_cause, id=id, buy_id=buy_id, sell_id=sell_id)
        return cb_entrust_info

    def update_entrust(self, entrust_info: CombOrderDataImpl, entrust_type: PushType):
        cb_entrust_info: CombOrderDataImpl = self._cb_entrust_info_dict.get(entrust_info.internal_id, None)
        if cb_entrust_info is not None:
            self._cb_entrust_info_dict[entrust_info.internal_id] = cb_entrust_info
        else:
            python_logger.debug(
                f"该子单尚未加入管理，添加这笔子单。方案：{self._scheme.scheme_id}子单号：{entrust_info.internal_id}")

        is_final_state = self._if_keep_final_state_entrust()
        if not is_final_state and (
                entrust_type == PushType.ORDER_FAIL or self.is_final_state(entrust_info=entrust_info)):
            self.del_entrust(internal_id=entrust_info.internal_id)

    def is_final_state(self, entrust_info: CombOrderDataImpl):
        if ((entrust_info.status == OrderStatus.WASTE or
             entrust_info.status == OrderStatus.FILLED or
             entrust_info.status == OrderStatus.CANCELLED or
             entrust_info.status == OrderStatus.PARTCANCELLED) and
                (entrust_info.buy_status == OrderStatus.WASTE or
                 entrust_info.buy_status == OrderStatus.FILLED or
                 entrust_info.buy_status == OrderStatus.CANCELLED or
                 entrust_info.buy_status == OrderStatus.PARTCANCELLED) and
                (entrust_info.sell_status == OrderStatus.WASTE or
                 entrust_info.sell_status == OrderStatus.FILLED or
                 entrust_info.sell_status == OrderStatus.CANCELLED or
                 entrust_info.sell_status == OrderStatus.PARTCANCELLED)):
            return True
        else:
            return False

    def _if_keep_final_state_entrust(self) -> bool:
        """
        判断是否保留终态委托
        :return:True 保留，否则不保留
        """
        return self._scheme.keep_final_state_entrust

    def find_entrust(self, internal_id: str) -> CombOrderData:
        """
        从字典中找委托记录
        :param internal_id:子单号
        :return:CombOrderData,找不到返回默认None
        """
        return self._cb_entrust_info_dict.get(internal_id, None)

    def get_iterator(self, security_detail_id: str = ""):
        """
        返回方案明细的迭代列表
        :param security_detail_id:方案明细序代码
        :return:
        """
        if security_detail_id == "":
            for entrust in self._cb_entrust_info_dict.values():
                yield entrust
        else:
            for entrust in self._cb_entrust_info_dict.values():
                if entrust.security_detail_id == security_detail_id:
                    yield entrust

    def get_entrust_list(self):
        return self._cb_entrust_info_dict.values()
