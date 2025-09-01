# -- coding: utf-8 --
from typing import Dict, List

from qt_strategy_base import PCJHqInfo, PQDBJHqInfo, BondCalcData
from qt_strategy_base.common.singleton import singleton


@singleton
class BondPriceCalcManage:
    def __init__(self):
        self._net_price_dict: Dict[str, BondCalcData] = {}
        self._ytm_dict: Dict[str, BondCalcData] = {}
        self._ytc_dict: Dict[str, BondCalcData] = {}

    def get_by_key(self, price_key: str, key_type: int):
        if key_type == 1:
            bond_price = self._net_price_dict.get(price_key, None)
            return bond_price
        elif key_type == 2:
            bond_price = self._ytm_dict.get(price_key, None)
            return bond_price
        elif key_type == 3:
            bond_price = self._ytc_dict.get(price_key, None)
            return bond_price

    def add_or_update(self, price_key: str, key_type: int, bond_price: BondCalcData):
        if key_type == 1:
            self._net_price_dict[price_key] = bond_price
        elif key_type == 2:
            self._ytm_dict[price_key] = bond_price
        elif key_type == 3:
            self._ytc_dict[price_key] = bond_price
