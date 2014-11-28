#coding=utf-8
'''
Created on 2014年8月10日
用户管理api视图类
@author: tubin
'''
from rest_framework.response import Response
from users.api.serializers import UserSerializer, AuthTokenSerializer
from rest_framework import status
from rest_framework.views import APIView
from core import contenttype
import logging
from rest_framework.permissions import IsAuthenticated
from users.models import MToken

log=logging.getLogger("user.logger")



class Login(APIView):
    '''
            登录api
    '''
    def post(self, request):
        data={}
        terminal=request.DATA.get('terminal',None)
        version=request.DATA.get('version',None)
        if terminal and version:
            serializer = AuthTokenSerializer(data=request.DATA) 
            if serializer.is_valid(): 
                user=serializer.object['user']
                do_login(user, int(terminal), float(version), data)
                data['last_login_time']=user.last_login
                log.info("%s login with app! terminal=%s",user.username,terminal)
            else:
                data[contenttype.RESULT]=1
                data[contenttype.MSG]=serializer.errors.get('non_field_errors',None)[0]
        else:
            data[contenttype.RESULT]=contenttype.DATA_ERROR
        return Response(data, status=status.HTTP_200_OK) 

def do_login(user,terminal,version,data):
    '''
    登录处理
    '''
    token = MToken.get_or_create(user=user,terminal=terminal,version=version)
    log=logging.getLogger("user.logger")
    log.info("%s login with app!",user.username)
    data[contenttype.RESULT]=0
    data[contenttype.TOKEN]=token.key
    data['user']=UserSerializer(user).data
    user.incr_login_num()
    
# @authentication_classes((SessionAuthentication, BasicAuthentication))
class Logout(APIView): 
    '''
            注销api
    '''
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        request.auth.delete() 
        return Response({contenttype.RESULT:0})

