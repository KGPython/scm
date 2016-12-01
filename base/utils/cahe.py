from django.conf import settings
from django.core.cache import cache
import json
#read cache user id
def read_from_cache(self, user_name):
    key = 'user_id_of_'+user_name
    value = cache.get(key)
    if value == None:
        data = None
    else:
        data = json.loads(value)
    return data
#write cache user id
def write_to_cache(self, user_name):
    key = 'user_id_of_'+user_name
    cache.set(key, json.dumps(user_name), settings.NEVER_REDIS_TIMEOUT)