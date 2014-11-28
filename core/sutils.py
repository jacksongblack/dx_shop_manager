#coding=utf-8
'''
Created on 2014年10月13日

@author: tubin
'''

def get_data_ditc(request):
    data={}
    if request.user and request.user.is_authenticated():
        data['username']=request.user.username
    return data