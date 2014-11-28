#coding=utf-8
'''
Created on 2014年9月17日
基本模型
@author: tubin
'''
from core.modelcache import ModelWithCache
import os
import time
import random
from django.db import models
from utils.uuid import uuid

class BaseModel(ModelWithCache): 
    '''
    基本model
    '''
    '''
    带缓存的model
    '''
    id =models.CharField(max_length=32,unique=True,primary_key=True,default=None,editable=False)
    def save(self, *args, **kwargs): 
        if self.id is None or self.id==0:
            self.id=uuid()
        super(BaseModel, self).save() 
        
    def get_upload_path(self,filename):
        '''获取上传文件路径'''
        return 'upload/%s/%s' % (self.id, filename)
    
    class Meta:
        abstract=True 
 
class BaseModelNoCache(models.Model): 
    '''
    基本model
    '''
    '''
    带缓存的model
    '''
    id =models.CharField(max_length=32,unique=True,primary_key=True,default=None,editable=False)
    def save(self, *args, **kwargs): 
        if self.id is None or self.id==0:
            self.id=uuid()
        super(BaseModelNoCache, self).save() 
        
    def get_upload_path(self,filename):
        '''获取上传文件路径'''
        return 'upload/%s/%s' % (self.id, filename)
    
    class Meta:
        abstract=True
           
def get_file_path(model, filename):
    '''
    获取上传文件路径
    '''
    if isinstance(model, BaseModel) or isinstance(model, BaseModelNoCache):
        return model.get_upload_path(make_filename(filename))
    return 'upload/commons/%s' % (make_filename(filename))

def make_filename(filename):
    '''
    重新生成文件名
    '''
    #文件扩展名
    ext = os.path.splitext(filename)[1]
#     #文件目录
#     d = os.path.dirname(filename)
    #定义文件名，年月日时分秒随机数
    fn = time.strftime("%Y%m%d%H%M%S")
    fn = fn + "_%d" % random.randint(0,100) 
    #重写合成文件名
#     return os.path.join(d, fn + ext)
    return fn + ext

def change_image_path(path,terminal):
    '''
    移动端图片路径转换
    '''
    if path is None or path=='':
        return path
    if terminal:
        i=path.rindex("/")
        return path[:i] + '/'+str(terminal) + path[i:]
