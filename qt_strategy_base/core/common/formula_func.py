# -- coding: utf-8 --
from qt_strategy_base.core.model.model import PSecurityBaseInfo
from qt_strategy_base.model.strategy_api_data import SecurityBaseInfo


def calc_balance(stock_info: SecurityBaseInfo, price: float, amount: float) -> float:
    # if stock_info.security_type == SecurityType.BOND_REPURCHASE:  # 回购
    # balance = stock_info.face_value * amount
    # else:
    balance = price * stock_info.contract_multiplier * amount
    return balance
