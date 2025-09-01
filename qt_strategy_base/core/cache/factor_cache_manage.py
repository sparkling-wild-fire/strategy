# -- coding: utf-8 --
from typing import Dict, List
from qt_strategy_base.common.singleton import singleton


@singleton
class FactorCacheManageBase:
    def __init__(self):
        self._subscribe_cache_dict: Dict[str, List[int]] = {}  # 主键为代码+因子名称，值为订阅该券的方案列表

    def query_subscribe_by_itemkey(self, item_key) -> List[int]:
        subscribe_scheme_id_list: List[int] = self._subscribe_cache_dict.get(item_key, [])
        return subscribe_scheme_id_list

    def add_or_update_subscribe_by_itemkey(self, item_key: str, scheme_id: int):
        if item_key in self._subscribe_cache_dict.keys():
            if scheme_id not in self._subscribe_cache_dict[item_key]:
                self._subscribe_cache_dict[item_key].append(scheme_id)
        else:
            self._subscribe_cache_dict[item_key] = [scheme_id]

    def get_un_subscribe_list_by_scheme_id(self, scheme_id: int) -> List[str]:
        unsubscribe_list = []
        for full_code, scheme_id_list in self._subscribe_cache_dict.items():
            if scheme_id in scheme_id_list:
                if len(scheme_id_list) == 1:
                    unsubscribe_list.append(full_code)
                else:
                    scheme_id_list.remove(scheme_id)
        for item in unsubscribe_list:
            del self._subscribe_cache_dict[item]
        return unsubscribe_list


