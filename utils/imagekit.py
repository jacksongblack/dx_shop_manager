#coding=utf-8
'''
Created on 2014年9月24日
图片处理工具
@author: tubin

'''
from PIL import Image
from config import MEDIA_API_URL
import os

def thumb_image_file(srcfile,width,height,tagpath,name):
    '''
    压缩图片
    '''
    if not os.path.isdir(tagpath):    
        os.makedirs(tagpath)
    if os.path.isfile(tagpath+name):    
        return
        
    pixbuf=Image.open(srcfile)
    w,h = pixbuf.size

    if w > width:
        delta = w / width
        height = int(h / delta)
        pixbuf.thumbnail((width, height), Image.ANTIALIAS)
    pixbuf.save(tagpath+name)

def resize(srcfile,tagfile,width,height):
    '''
    图片大小压缩
    '''
    img = Image.open(".."+MEDIA_API_URL+srcfile)
    img = img.resize((width,width),Image.ANTIALIAS)
    img.save(".."+MEDIA_API_URL+tagfile)