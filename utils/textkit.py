#coding=utf-8
'''
Created on 2014年10月10日

@author: tubin
'''
STAR_STR="****"

def hide_phone_str(phone):
    '''
    隐藏手机号码
    '''
    if phone and len(phone)>7:
        return phone[0:3]+STAR_STR+phone[7:]