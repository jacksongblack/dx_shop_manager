# coding=utf-8
'''
Created on 2014年8月26日
自定义用户验证方法，支持邮件和手机号码登录
@author: tubin
'''

from django.contrib.auth.backends import ModelBackend
from users.models import User

class CheckModelBackend(ModelBackend):
    '''
    自定义用户验证方法，支持用户名登录
    '''
    def authenticate(self, username = None, password = None):
        if username and password:
            try:
                user = User.objects.get(username = username)
                if user and user.is_active and user.check_password(password):
                    return user
                return None
            except User.DoesNotExist:
                return None
