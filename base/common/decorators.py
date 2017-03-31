# -*-  coding:utf-8 -*-
from functools import wraps
from django.template.loader import render_to_string
from django.core.cache import caches
from base.utils import MethodUtil as mtu

def d_table_check_sum(template_name=None):
    def decorator(func):
        def wrapper(*args, **kw):
            print('cache')
            if caches['redis2'].get('test'):
                return func(*args, **kw)
            else:
                caches['redis2'].set('test','aaaaa')
                return func(*args, **kw)
        return wrapper
    return decorator