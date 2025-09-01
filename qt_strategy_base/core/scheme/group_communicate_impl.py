# -*- coding: utf-8 -*-
from qt_strategy_base.api.strategy_api_model import GroupCommication
from qt_strategy_base.core.common.notice_sever import  NoticeServer
from qt_strategy_base.core.common.aglo_function_impl import  FunctionImpl
from qt_strategy_base.model.error_info import ErrorInfo
from qt_strategy_base.core.scheme.strategy_scheme_impl import  ContextImpl
from  qt_strategy_base.core.model.base import  BaseObject
from qt_strategy_base.api.strategy_api_model import GroupMsg

class GroupCommication(GroupCommication):

    def __init__(self):
        self._group_name=""
        self._function= None
        self._scheme_context:ContextImpl = None
        self._group_id=0

    @property
    def group_name(self) -> str:
        """
        组名
        """
        return self._group_name

    def close(self):
        """
        释放链接，退出当前的group
        @return:
        """
        if self._group_name != "" and self._scheme_context is not None:
            NoticeServer.cancel_group_suber(self._scheme_context.scheme_id,self._group_name)
            self._scheme_context._group_mange.close_group(self._group_name)
            self._group_name= ""
            self._scheme_context= None
            self._function= None


    def push_msg(self,key:str,data,data_length:int,type_name:str):
        """
        推送策略组的组消息
        @param key: 消息的key值，不允许超过128个字符
        @param data: 数据对象，
        @param data_lenght:数据对象的长度
        @param type_name:数据对象的名称，数字为 'I',浮点数为 'D'，字符传 'S'
        @return:
        """
        NoticeServer.group_msg_push(key,data,data_length,type_name,self._scheme_context.scheme_id,self._group_name,self._group_id)

class GroupManager(BaseObject):
    def __init__(self,scheme_context:ContextImpl):
        self._group_cahce={}
        self._context= scheme_context

    def close(self):
        for item in self._group_cahce.values():
            item.close()
        self._group_cahce.clear()


    def new_group_commictiaon(self,groug_name:str,function) ->ErrorInfo:
        error ,group_id= FunctionImpl.group_communicate_register(groug_name)
        if error.has_error():
            return error,None
        groug_info = GroupCommication()
        groug_info._group_name = groug_name
        groug_info._function = function
        groug_info._scheme_context =  self._context
        groug_info._group_id= group_id
        self._group_cahce.setdefault(groug_name,groug_info)
        return error,groug_info
    def close_group(self,group_name):
        self._group_cahce.pop(group_name,None)

    def group_msg_update(self,group_msg_data):
        from qt_strategy_base.model.strategy_api_data import GroupMsgData
        temp= GroupMsgData(group_msg_data)
        if  group_msg_data.group_name in self._group_cahce:
            group_info=self._group_cahce[group_msg_data.group_name]
            group_info._function(self._context, group_info,temp)
