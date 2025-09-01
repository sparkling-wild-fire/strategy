# -*- coding: utf-8 -*-
from enum import Enum


class FunctionID(Enum):
    CreateScheme = 10000

    Login = 20000
    OnSchemeCancelReq = 10001  # 方案撤销请求
    OnSchemeCancelled = 10002  # 方案撤销
    OnSchemePaused = 10003  # 方案暂停
    OnSchemeResume = 10004  # 方案恢复运行
    OnEntrustReqAccept = 10005  # 本地创建委托单时回调该函数
    OnEntrustReqReject = 10006  # 子单委托被投资系统拒绝时回调该函数
    OnEntrustConfirm = 10007  # 子单委托确认回调该函数
    OnTrade = 10008  # 子单委托收到成交消息时回调该函数
    OnEntrustWaste = 10009  # 子单委托废单时回调该函数

    '''
    公共框架发出请求后回调该函数，传给委托对象及原委托数量
    注意在以下场景下公共框架会将请求的委托分拆为多笔委托:
    1.上期所或能交所合约未指定平仓方向时
    2.委托数量超过最大委托数量时
    每笔分拆出的委托都将回调该函数, 所有委托数量总和等于原委托数量
    '''

    OnEntrustCancelled = 10010  # 子单委托收到撤成消息时回调该函数
    OnEntrustWithdrawFailed = 10011  # 子单撤单失败时回调该函数（需设置SetCancelOnce）
    OnHqReceive = 10012  # 行情回调
    OnSchemeRelease = 10013  # 方案释放

    HoldUpdateCallback = 10017
    EntrustPush = 10018
    DealPush = 10019
    MktDutyPush = 10020
    CBEntrustPush = 10021
    OnCBEntrustReqAccept = 10022
    OnCBEntrustReqReject = 10023  # 上游系统的
    # 明细恢复
    SchemeStockResume = 10024
    # 明细暂停
    SchemeStockPaused = 10025
    # 明细撤销
    SchemeStockCancel = 10026
    StrategyParamModify = 10027
    # 委托错误应答
    EntrustErrorReturn = 10028
    # etf申购成交消息
    EtfRealDel = 10029
    # 明细控制接口
    SchemeStockCtrl = 10030
    # 委托恢复
    EntrustRecovery = 10031
    # 点击行情回调
    OnQDBJHqReceive = 10032
    # 成交行情回调
    OnCJHqReceive = 10033
    SendTcpStatus = 20001

    GetHqBatch = 20003

    SubHqBatch = 20005
    SendEntrustReq = 20006

    GetHoldList = 20008
    CancelEntrustBySubID = 20009
    GetOrderIdStart = 20010  # 获取新的order标识字符串

    SystemMessage = 20012
    CallBackThreadException = 20013
    CallSchemeOverdue = 20014
    CallSchemeFinished = 20015
    CallSchemePause = 20016
    CallSchemeRun = 20017
    CallSchemeCanceled = 20018
    AddHoldSub = 20019
    ReleaseHoldSub = 20020
    AddEntrustSub = 20021
    ReleaseEntrustSub = 20022
    AddDealSub = 20023
    ReleaseDealSub = 20024
    AddMktDutySub = 20025
    ReleaseMktDutySub = 20026
    AddCbEntrustSub = 20027
    ReleaseCbEntrustSub = 20028
    SendCBEntrustReq = 20029
    CancelCBEntrustReq = 20030

    GetBondProperty = 20031
    GetFutureInfo = 20032
    GetOptionInfo = 20033
    GetEtfStocks = 20034
    GetEtfInfo = 20035
    SetCancelOnce = 20036
    UnSubscribeHQ = 20037


    PushKeyValueCount = 20039
    SendLogMessage = 20040
    GetStockInfo = 20041  # 批量查询证券基础信息

    SchemeStockStatusChange = 20042
    SubQDBJHq = 20043
    UnSubQDBJHq = 20044
    SubCJHq = 20045
    UnSubCJHq = 20046
    GetAccountFund = 20048
    GetOpenOrders = 20049
    GetTrades = 20050
    GetOptionInfoByTargetStock = 20110
    GetNEEQHq = 20104
    GetQDBJHq = 20105
    GetCJHq = 20106
    SendBondEntrustReq = 20107
    GetKLineDay = 20108
    GetKLine = 20109
    BondPricingCalc = 20047
    GetChinabondValuation = 20111
    GetAccount = 20113
    ScheduleCallBack = 30002
    ExtMessageCallBack = 30003
    SubFactor = 20141
    SubNonStandardFactor = 20142
    UnSubFactor = 20143
    UnSubNonStandardFactor = 20144
    GetFactor = 20145
    GetNonStandardFactor = 20145
    GetAlgoScheme = 20147
    RunAlgoScheme = 20148
    CancelAlgoScheme = 20149
    SubXBondHq = 20151
    UnSubscribeXBondHQ = 20152
    SubIntrabakBondMM = 20153
    UnSubIntrabakBondMM = 20154
    GetHisPosition = 20155
    GroupPermissionQRY=20156
    GroupMsgPush=20157
    UnsubroupCommuntion = 20158




    OnFactor = 10040
    OnNonStandardFactor = 10041
    AlgoSchemeUpdate = 10048
    AlgoSchemeDetailUpdate = 10049
    OnXBondHq = 10052
    OnIntrabakBondHq = 10053
    OnGroupMsgUpdate=10054


class FunctionType(Enum):
    CREATE = 1
    STOP = 2
    CALLBACK = 3
    QUERY = 4
    INNERCALLBACK = 5
    NOTICESERVER = 6
    BatchCALLBACK = 7


class ApiRetType(Enum):
    APIRETERR = -1
    APIRETOK = 0


MSGTYPE_ALGOJR_SCHEME_REMAIN = "asset.algo.scheme_remain"
MSGTYPE_ALGOJR_RECOVER_SCHEME = "asset.algo.recover_scheme"
