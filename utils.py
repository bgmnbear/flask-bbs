import os
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


def bbs_time(t):
    u_t = time.time()
    d_t = u_t - int(t)

    d = dict(
        second=1,
        minute=60,
        hour=3600,
        day=86400,
    )
    if 0 <= d_t < d['minute']:
        return '刚刚'
    elif d['minute'] <= d_t < d['hour']:
        return '{}分钟前'.format(int(d_t / d['minute']))
    elif d['hour'] <= d_t < d['day']:
        return '{}小时前'.format(int(d_t / d['hour']))
    elif d_t <= d['day'] * 3:
        return '{}天前'.format(int(d_t / d['day']))
    return date(t)


def log(*args, **kwargs):
    u_t = time.time()
    dt = date_time(u_t)
    with open('whister.log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, **kwargs)
        print(dt, *args, file=f, **kwargs)
