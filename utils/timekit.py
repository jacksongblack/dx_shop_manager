#coding=utf-8
'''
Created on 2014年9月25日
时间控件
@author: tubin
'''
DAY_SECONDS=3600*24

def get_differ_seconds(date1,date2):
    '''
    获取两个日期之间的时间差（秒）
    '''
    if date1>date2:
        dt=date1-date2
    elif date1<date2:
        dt=date2-date1
    else:
        return 0
    sec=dt.days*DAY_SECONDS
    return sec+dt.seconds
    
    
    