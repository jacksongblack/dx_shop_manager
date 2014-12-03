# coding=utf-8
'''
Created on 2014年8月8日
user模型
@author: tubin
'''
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, \
    SiteProfileNotAvailable, UserManager, Group
from django.core import validators
import re
from django.utils.translation import ugettext_lazy as _
import warnings
from django.core.exceptions import ImproperlyConfigured
from utils.uuid import uuid
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group
from plugin.decorators import handler
from plugin.image import Images


class User(AbstractBaseUser, PermissionsMixin):
    '''
    用户模型，暂时测试用
    '''
    id = models.CharField(max_length=32, unique=True, primary_key=True, default=None, editable=False)
    username = models.CharField(max_length=30, unique=True,
                                validators=[
                                    validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'),
                                                              'invalid')
                                ])
    email = models.EmailField(blank=True, max_length=30)
    phone = models.CharField(blank=True, max_length=11)
    login_num = models.IntegerField(default=0)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(blank=True, null=True)
    user_parent_id = models.CharField(max_length=32, blank=True, null=True)
    secure_phone = models.CharField(max_length=11, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    sex = models.SmallIntegerField(blank=True, null=True)
    address = models.CharField(default="", max_length=50)
    avatar = models.CharField(default="", max_length=100)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        db_table = 'user'
        swappable = 'AUTH_USER_MODEL'

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def incr_login_num(self, num=1):
        '''增加登录次数'''
        self.login_num += num
        self.save()

    def save(self, *args, **kwargs):
        if self.id is None or self.id == 0:
            self.id = uuid()
            super(User, self).save(*args, **kwargs)

    def set_goups(self, groups):
        self.groups.add(Group.objects.get(name=groups))

    @classmethod
    def create_user(cls, request):
        keys = ("username", "password", "address","email", "phone", "secure_phone", "email", "sex")
        data = dict(request.POST)
        for key in data.keys():
            if key not in keys and data.get(key):
                data.pop(key)
            else:
                data[key] = data.get(key, "")[0]
        data["avatar"] = Images(request.FILES.get("avatar","")).waterMark().save().get("waterMark","")
        user = User.objects.create_user(data.pop("username"), str(data.pop("email")), data.pop("password"), **data)
        user.set_goups(request.POST.get("permision_group"))
        user.save()
        return user

    @classmethod
    @handler
    def query_index(cls, request):
        '''
        index界面搜索方法,并防止数据库注入
        param query_dict: 搜索的参数
        param data: 数据库查询结果
        '''
        return ("id","username", "phone", "secure_phone", "sex")

    def get_profile(self):
        """
        Returns site-specific profile for this user. Raises
        SiteProfileNotAvailable if this site does not allow profiles.
        """
        warnings.warn("The use of AUTH_PROFILE_MODULE to define user profiles has been deprecated.",
                      DeprecationWarning, stacklevel=2)
        if not hasattr(self, '_profile_cache'):
            from django.conf import settings

            if not getattr(settings, 'AUTH_PROFILE_MODULE', False):
                raise SiteProfileNotAvailable(
                    'You need to set AUTH_PROFILE_MODULE in your project '
                    'settings')
            try:
                app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
            except ValueError:
                raise SiteProfileNotAvailable(
                    'app_label and model_name should be separated by a dot in '
                    'the AUTH_PROFILE_MODULE setting')
            try:
                model = models.get_model(app_label, model_name)
                if model is None:
                    raise SiteProfileNotAvailable(
                        'Unable to load the profile model, check '
                        'AUTH_PROFILE_MODULE in your project settings')
                self._profile_cache = model._default_manager.using(
                    self._state.db).get(user__id__exact=self.id)
                self._profile_cache.user = self
            except (ImportError, ImproperlyConfigured):
                raise SiteProfileNotAvailable
        return self._profile_cache


class MToken(Token):
    """
    移动登录token对象，用于标记用户登录相关信息
    """
    terminal = models.SmallIntegerField()
    version = models.DecimalField(max_digits=10, decimal_places=5)

    class Meta:
        db_table = 'auth_token'

    @staticmethod
    def get_or_create(user=None, terminal=None, version=None):
        try:
            token = MToken.objects.get(user_id=user.id)
        except:
            token = MToken.objects.create(user_id=user.id, terminal=terminal, version=version)
            return token

