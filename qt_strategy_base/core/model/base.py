# -*- coding: utf-8 -*-
from abc import ABC


class BaseObject(ABC):

    def __repr__(self):

        method_str = ""
        for name, obj in vars(self.__class__).items():
            if isinstance(obj, property):
                if method_str == "":
                    method_str = f'{name}={getattr(self, name)}'
                else:
                    method_str = method_str + f',{name}={getattr(self, name)}'
        return self.__class__.__name__ + f'({method_str})'
