# -*- coding: utf-8 -*-
from functools import wraps
from inspect import getfullargspec
from typing import get_type_hints


def ver(obj, **kwargs):
    hints = get_type_hints(obj)
    for params, params_types in hints.items():
        is_success = False
        if params != 'return':
            if not isinstance(params_types, list):
                params_types = [params_types]
            for param_type in params_types:
                if isinstance(kwargs[params], param_type):
                    is_success = True
        if not is_success:
            raise TypeError("参数：{} 类型错误，应该是:{} 类型".format(params, params_types))


def type_ver(dec):
    @wraps(dec)
    def wrapp(*args, **kwargs):
        # 通过反射拿到函数的参数
        fun_arg = getfullargspec(dec)
        # 参数，入参组和
        kwargs.update(dict(zip(fun_arg[0], args)))
        ver(dec, **kwargs)
        return dec(**kwargs)

    return wrapp
