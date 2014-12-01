#coding=utf-8
'''
Created on 2014年8月11日
用户登录form
@author: tubin
'''
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
# from captcha.fields import CaptchaField

class UserLoginForm(forms.Form):
    '''
    登录form,匹配用户名和密码
    '''
    username = forms.RegexField(label=_("Username"), max_length=30,
        regex=r'^[\w.@+-]+$',
        error_messages={
            'required':_("Username can not be null"),            
            'invalid': _("Username just can be email or phone nums")})
    password = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput, error_messages={
            'required':_("Password can not be null")})
    # captcha = CaptchaField()

class UserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.password.startswith('pbkdf2_sha256'):
            obj.set_password(obj.password)
        super(UserAdmin, self).save_model(request, obj, form, change)