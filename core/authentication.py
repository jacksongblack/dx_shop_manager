#coding=utf-8
'''
Created on 2014年10月16日
自定义移动端登录验证接口
@author: tubin
'''
from rest_framework.authentication import TokenAuthentication
from users.models import MToken

class MTokenAuthentication(TokenAuthentication):
    '''
    继承至TokenAuthentication，只改变模板对象
    '''
    model = MToken