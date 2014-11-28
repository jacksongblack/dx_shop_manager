#coding=utf-8
'''
Created on 2014年8月10日
用户序列号对象
@author: tubin
'''
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from users.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate

class AuthTokenSerializer(serializers.Serializer):
    '''
    用户权限序列化验证
    '''
    name = serializers.CharField()
    pwd = serializers.CharField()
    type = serializers.IntegerField()
    def validate(self, attrs):
        username = attrs.get('name')
        password = attrs.get('pwd')
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)
                attrs['user'] = user
                return attrs
            else:
                msg = _('Unable to login with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "username" and "password"')
            raise serializers.ValidationError(msg)



class UserSerializer(ModelSerializer):
    '''
    用户信息序列化
    '''
    class Meta:
        model = User
        fields = ('id', 'username', 'phone', 'email')
 
       
