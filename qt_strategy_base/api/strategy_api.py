# -*- coding: utf-8 -*-

from qt_strategy_base.api.strategy_api_context import ContextInfo
from qt_strategy_base.core.common.utility import virtual
from qt_strategy_base.model.error_info import ErrorInfo


class StrategyBase:

    @virtual
    def initialize(self, context: ContextInfo) -> ErrorInfo:
        """返回初始化失败的原因，该信息将会推送到前台展示"""
        return ErrorInfo.ok()
