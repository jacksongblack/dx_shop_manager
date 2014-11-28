#coding=utf-8
'''
Created on 2014年8月29日

@author: tubin
'''
from django.core.cache import cache 
from django.db import models 
from dx_shop_manager import settings

DOMAIN_CACHE_PREFIX = settings.CACHE_MIDDLEWARE_KEY_PREFIX 
CACHE_EXPIRE = settings.CACHE_MIDDLEWARE_SECONDS 

def cache_key(model, uid):
    '''
    获取缓存key
    ''' 
    return ("%s-%s-%s" % (DOMAIN_CACHE_PREFIX, model._meta.db_table, uid)).replace(" ", "") 


class MCacheManager(models.Manager): 
    '''
    to reload the get method. cache -> db -> cache 
    '''
    def get(self, *args, **kwargs): 
        uid = repr(kwargs) 
        model_key = cache_key(self.model, uid) 
        model = cache.get(model_key) 
        if model != None: 
            return model 
        try:
            model = super(MCacheManager, self).get(*args, **kwargs) 
            model_key = cache_key(model, model.pk) 
            cache.set(model_key, model, CACHE_EXPIRE) 
            return model 
        except BaseException,e:
            print e
            raise e
        
class ModelWithCache(models.Model): 
    objects = MCacheManager()
    
    def save(self, *args, **kwargs): 
        # first, delete cache {model_key -> model} 
        model_key = cache_key(self, self.pk) 
        cache.delete(model_key) 
        super(ModelWithCache, self).save() 

    # to reload the delete method 
    def delete(self, *args, **kwargs): 
        # first, delete cache {model_key -> model} 
        model_key = cache_key(self, self.pk) 
        cache.delete(model_key) 
        super(ModelWithCache, self).delete()
        
    class Meta:
        abstract=True 
