 # -- coding: utf-8 --
from qt_strategy_base.core.cache.global_params import GlobalParams
from qt_strategy_base.core.cache.scheduler_manage import SchedulerManger
from qt_strategy_base.core.common.notice_sever import NoticeServer

from qt_strategy_base.model.enum import ScheduleType, MessageType, Setting
from qt_strategy_base.model.error_info import ErrorInfo
from  qt_strategy_base.api.strategy_api_model import GroupCommication

def pause(remark: str = "", is_cancel_order: bool = False):
    """
    方案暂停,初始化不支持
    @param remark:方案暂停备注
    @param is_cancel_order:是否撤单
    @return:Non
    """
    NoticeServer.scheme_pause(scheme_id=0, is_cancel_order=is_cancel_order, message=remark)


def resume(remark: str = ""):
    """
    方案恢复运行,初始化不支持,暂停回调不支持
    @param remark: 方案恢复运行备注
    @return:
    """
    NoticeServer.scheme_resume(scheme_id=0, message=remark)


def finish(remark: str = ""):
    """
    方案结束,初始化不支持
    @param remark: 方案结束备注
    @return:
    """
    NoticeServer.scheme_finished(scheme_id=0, message=remark)


def schedule_execute(type: ScheduleType, function, time: str = 0, seconds: int = 0, start_time: str = "",
                     end_time: str = "") -> str:
    """
    定时器
    @param type: 定时类型 固定时间运行：FIXED，固定间隔运行：INTERVAL
    @param function:定时执行的函数
    @param time: 固定运行的时间,时间格式HH:MM:SS
    @param seconds:间隔多少秒
    @param start_time:开始时间,时间格式HH:MM:SS
    @param end_time:结束时间,时间格式HH:MM:SS
    @return:任务id
    """
    scheduler_manger: SchedulerManger = SchedulerManger()
    if type == ScheduleType.FIXED:
        return scheduler_manger.add_one_schedule(target_time=time, function=function)
    elif type == ScheduleType.INTERVAL:
        return scheduler_manger.add_schedule(seconds=seconds, start_time=start_time, end_time=end_time,
                                             function=function)


def cancel_schedule(scheduler_id: str = None):
    """
    取消定时运行
    @param scheduler_id: 任务id
    @return:
    """
    scheduler_manger: SchedulerManger = SchedulerManger()
    scheduler_manger.cancel_schedule(scheduler_id=scheduler_id)


def send_message(content: str, message_type=MessageType.INFO):
    """
    给前台发日志
    @param content:日志内容
    @param message_type:日志级别
    @return:
    """
    NoticeServer.send_message(content=content, message_type=message_type)


def set_option(setting: Setting, flag: bool):
    """
    方案参数设置
    @param setting: 要设置的参数
    @param flag: 参数内容
    @return: 
    """

    current_scheme_id = GlobalParams().current_scheme_id
    from qt_strategy_base.core.cache.scheme_manage import SchemeManage
    current_scheme = SchemeManage().get_scheme(scheme_id=current_scheme_id)
    if setting == Setting.SHOW_FINISHED_ORDER:
        current_scheme.keep_final_state_entrust = flag
    elif setting == Setting.REPEAT_CANCEL:
        current_scheme.cancel_once = not flag


def cancel_order(internal_id: str) -> ErrorInfo:
    """
    单笔撤单
    @param internal_id: 内部委托号
    @return:错误信息
    """
    current_scheme_id = GlobalParams().current_scheme_id
    from qt_strategy_base.core.cache.scheme_manage import SchemeManage
    current_scheme = SchemeManage().get_scheme(scheme_id=current_scheme_id)
    if current_scheme is not None:
        return current_scheme.cancel_order_by_internal_id(order_id=internal_id)
    else:
        return ErrorInfo.bad(error_msg="撤单失败原因，当前方案查找失败！")


def cancel_comb_order(internal_id: str = "", order_id: int = 0) -> ErrorInfo:
    """
    合笔委托
    @param internal_id: 内部委托号
    @param order_id: 对接系统委托号
    @return:错误信息
    """
    error_info = ErrorInfo()
    if internal_id == "" and order_id == 0:
        error_info.set_error_value("internal_id和order_id不能同时为空")
        return error_info
    current_scheme_id = GlobalParams().current_scheme_id
    return NoticeServer.cancel_comb_order(scheme_id=current_scheme_id, internal_id=internal_id, order_id=order_id)


def message_push(data):
    """
    推送数据触发on_message回调
    @param data:任何类型的数据
    @return:
    回调函数on_message(self, context: ContextInfo, data)
    """

    from qt_strategy_base.core.scheme.ext_message_handle import ExtMessageManager
    ExtMessageManager().message_push(data)

def regiest_group_communication(group_name:str,function ) ->[ErrorInfo,GroupCommication]:
    """
    注册组的策略间的消息通讯组
    @param group_name: 组名
    @param function:收到同组消息回调的处理机制 ,(context,group_info,group_msg)
    @return:
    """

    current_scheme_id = GlobalParams().current_scheme_id
    from qt_strategy_base.core.cache.scheme_manage import SchemeManage

    current_scheme = SchemeManage().get_scheme(scheme_id=current_scheme_id)
    if current_scheme is not None:
        from qt_strategy_base.core.scheme.group_communicate_impl import GroupCommication
        return current_scheme._group_mange.new_group_commictiaon(group_name,function)
    else:
        return ErrorInfo.bad(error_msg="当前方案查找失败！"),None


def group_param_push(key:str,param_value,length:int,type_name:str,index:int=0):
    """
    推送策略间的消息
    @param key: 参数标识
    @param param_value: 参数值
    @param length:value的长度，I,S,D 类型可以不传入
    @param type_name: 参数类型
    @param index: 参数编号，本地设置
    @return:
    """
    pass
