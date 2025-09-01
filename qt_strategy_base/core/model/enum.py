# -- coding: utf-8 --
from enum import Enum


class LogSource(Enum):
    FRAMEWORK = 0
    CUSTOMER = 1


class EMessageType(Enum):
    LESS = 0
    FATAL = 1
    ERROR = 2
    WARNING = 3

    PERFORM = 4
    INFO = 5

    FLOW = 6
    DEBUG = 7
