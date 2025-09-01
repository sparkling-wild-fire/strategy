# -*- coding: UTF-8 -*
from pandas import DataFrame
from qt_strategy_base.core.model.base import BaseObject
from qt_strategy_base.core.scheme.strategy_scheme_stock_impl import SecurityDetail
from qt_strategy_base.model.enum import SchemeType

class GroupMsg(BaseObject):
    @property
    def group_name(self) -> str:
        """
        组名
        """
        pass

    @property
    def group_id(self)->int:
        """
        通讯组ID
        @return: ID
        """
        pass

    @property
    def key(self) -> str:
        """
        msg的key值
        """
        pass

    @property
    def type_name(self)->str:
        """
        数据对象的名称，数字为 'I',浮点数为 'D'，字符传 'S
        """
        pass

    @property
    def data_lenght(self) -> int:
        """
        数据对象的长度
        """
        pass

    @property
    def  data(self):
        """
        数据对象，如果是’I‘，会转化成int ,'S' 会转化成 字符串，’D‘,会转化成float,如果转化失败，会变成默认值
        """
        pass


class GroupCommication(BaseObject):
    @property
    def group_name(self) -> str:
        """
        组名
        """
        pass

    def close(self):
        """
        释放链接，退出当前的group
        @return:
        """
        pass
    def push_msg(self,key:str,data,data_lenght:int,type_name:str):
        """
        推送策略组的组消息
        @param key: 消息的key值，不允许超过128个字符
        @param data: 数据对象，
        @param data_lenght:数据对象的长度
        @param type_name:数据对象的名称，数字为 'I',浮点数为 'D'，字符传 'S'
        @return:
        """