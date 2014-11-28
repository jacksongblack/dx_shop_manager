#coding=utf-8
'''
Created on 2014年9月4日
唯一id生成器
@author: tubin
'''
import datetime
from django.core.cache import cache
from config import SERVER_ID
from core.contenttype import GID_KEY

def uuid():
    '''
    获取唯一id（订单使用）：日期时间+服务器编号+流水号
    '''
    sid=str(get_gid())
    sid=sid.zfill(6)
    uuid=datetime.datetime.now().strftime("%y%m%d%H%M%S")
    uuid=uuid+str(SERVER_ID)+sid
    return uuid

def get_gid():
    '''
    获取自增变量
    '''
    if not cache._client.exists(GID_KEY):
        cache.set(GID_KEY,1)
    gid=cache._client.incr(GID_KEY,1)
    if gid>=100000:
        gid=1
        cache.set(GID_KEY,1)
    return gid
