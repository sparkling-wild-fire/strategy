# -*- coding: utf-8 -*-
_FCMP: float = 0.00001
_DCMP: float = 0.0000001


def fbg(x: float, y: float) -> bool:
    """
    左边大于右边
    :param x:
    :param y:
    :return:
    """
    return True if (x - y) > (_FCMP if x > 10 else _DCMP) else False  # （比较俩个float值，如果x>y并且 x>10时取低精度，否则比较时取高精度)


def fls(x: float, y: float) -> bool:
    """
    左边小于右边
    :param x:
    :param y:
    :return:
    """
    return fbg(y, x)  # (注：实现上调转了 x，y的位置)


def fleq(x: float, y: float) -> bool:
    """
    左边小于或等于右边
    :param x:
    :param y:
    :return:
    """
    return not fbg(x, y)


def fbeq(x: float, y: float) -> bool:
    """
    左边大于或等于右边
    :param x:
    :param y:
    :return:
    """
    return not fls(x, y)


def feq(x: float, y: float) -> bool:
    """
     比较两个数字是否相等
    """
    return True if abs(x - y) < (_FCMP if x > 10 else _DCMP) else False


def trunc_ex(f: float) -> int:
    """
    取整
    """
    if f > 0:
        return int(f + 0.000001)
    else:
        return int(f - 0.000001)
