# -- coding: utf-8 --
from typing import Dict, List

from qt_strategy_base import PCJHqInfo, PQDBJHqInfo
from qt_strategy_base.common.singleton import singleton


@singleton
class BondHQCacheManageBase:
    def __init__(self):
        self._qdbj_hq_cache_dict: Dict[str, dict] = {}
        self._cj_hq_cache_dict: Dict[str, PCJHqInfo] = {}

        self._bond_click_subscribe_cache_dict: Dict[str, List[int]] = {}  # 主键为代码，值为订阅该券的方案列表

    def query_qdbj_hq_by_itemkey(self, item_key) -> dict:
        hq: dict = self._qdbj_hq_cache_dict.get(item_key, None)
        return hq

    def add_or_update_qdbj_hq_by_itemkey(self, item_key: str, hq: dict):
        self._qdbj_hq_cache_dict[item_key] = hq

    def query_cj_hq_by_itemkey(self, item_key) -> PCJHqInfo:
        hq: PCJHqInfo = self._cj_hq_cache_dict.get(item_key, None)
        return hq

    def add_or_update_cj_hq_by_itemkey(self, item_key: str, hq: PCJHqInfo):
        self._cj_hq_cache_dict[item_key] = hq

    def query_bond_click_subscribe_by_itemkey(self, item_key) -> List[int]:
        subscribe_scheme_id_list: List[int] = self._bond_click_subscribe_cache_dict.get(item_key, [])
        return subscribe_scheme_id_list

    def add_bond_click_subscribe_by_itemkey(self, item_key: str, scheme_id: int):
        if item_key in self._bond_click_subscribe_cache_dict.keys():
            if scheme_id not in self._bond_click_subscribe_cache_dict[item_key]:
                self._bond_click_subscribe_cache_dict[item_key].append(scheme_id)
        else:
            self._bond_click_subscribe_cache_dict[item_key] = [scheme_id]

    def remove_bond_click_subscribe_by_itemkey(self, item_key: str, scheme_id: int):
        if item_key in self._bond_click_subscribe_cache_dict.keys():
            if scheme_id in self._bond_click_subscribe_cache_dict[item_key]:
                self._bond_click_subscribe_cache_dict[item_key].remove(scheme_id)

    def get_unsubscribe_list_by_scheme_id(self, scheme_id: int) -> List[str]:
        unsubscribe_list = []
        for full_code, scheme_id_list in self._bond_click_subscribe_cache_dict.items():
            if scheme_id in scheme_id_list:
                if len(scheme_id_list) == 1:
                    unsubscribe_list.append(full_code)
                else:
                    scheme_id_list.remove(scheme_id)
        for item in unsubscribe_list:
            del self._bond_click_subscribe_cache_dict[item]
        return unsubscribe_list
