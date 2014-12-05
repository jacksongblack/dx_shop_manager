from django.core.cache import cache


class CacheFactory(object):
    def index_cache(self, request, after_failure_func, **params):
        cache_key = str(request.GET)
        data = cache.get(cache_key)
        if not data:
            if len(params):
                data = after_failure_func(**params)
            else:
                data = after_failure_func(request)
            cache.set(cache_key, data)
        return data

