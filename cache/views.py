#-*- coding:utf-8 -*-
__author__ = 'liubf'

from django.conf import settings
from django.core.cache import cache
import json
#read cache by key
def read_from_cache(self, key):
    value = cache.get(key)
    if value == None:
        data = None
    else:
        data = json.loads(value)
    return data
#write cache key,value
def write_to_cache(self,key,value):
    cache.set(key, json.dumps(value), settings.NEVER_REDIS_TIMEOUT)