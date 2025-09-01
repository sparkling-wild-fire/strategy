# -*- coding: utf-8 -*-
import threading


def singleton(cls):
    instance = {}
    lock = threading.Lock()

    def __single(*args, **kwargs):
        if cls not in instance:
            with lock:
                if cls not in instance:
                    instance[cls] = cls(*args, **kwargs)
        return instance[cls]

    return __single
