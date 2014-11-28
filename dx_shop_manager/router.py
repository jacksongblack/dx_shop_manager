# coding=utf-8

'''
Created on 2014年8月26日
配置多数据源
@author: tubin
'''

class DBRouter(object):

    def db_for_read(self, model, **hints):
        return self.__app_router(model)

    def db_for_write(self, model, **hints):
        return self.__app_router(model)

    def allow_relation(self, obj1, obj2, **hints):
#         if obj1._meta.app_label == obj2._meta.app_label:
        return True


    def allow_syncdb(self, db, model):
        '''
        该方法定义数据库是否能和名为db的数据库同步
        '''
        return self.__app_router(model) == db

    def __app_router(self, model):
        '''
        添加一个私有方法用来判断模型属于哪个应用，并返回应该使用的数据库
        '''
        if model._meta.app_label in ('users'):
            return 'default'
        else:
            return 'default'
