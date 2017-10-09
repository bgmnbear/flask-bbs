import os.path
import time
import json


def date_time(t):
    format = '%H:%M:%S'
    value = time.localtime(int(t))
    dt = time.strftime(format, value)
    return dt


def date(t):
    format = '%Y-%m-%d'
    value = time.localtime(int(t))
    d = time.strftime(format, value)
    return d


def log(*args, **kwargs):
    u_t = time.time()
    dt = date_time(u_t)
    with open('whister.log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, **kwargs)
        print(dt, *args, file=f, **kwargs)
