# coding=utf-8

from users.forms import UserLoginForm
from core import contenttype
from django.shortcuts import render_to_response
from django.contrib import auth
import logging
from django.views.generic.detail import DetailView
from users.models import User
from django.contrib.auth.models import Group
from django.views.generic.base import View
from django.template.context import RequestContext
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import loader

log = logging.getLogger("user.logger")
index_template = loader.get_template("user/index.html")
# Create your views here.
def login(request):
    '''
   登录
    '''
    data = {}
    if request.method == 'GET':
        form = UserLoginForm()
        data['form'] = form
    elif request.method == 'POST':
        form = UserLoginForm(request.POST)
        data['form'] = form
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                user.incr_login_num()
                log.info("%s login!", user.username)
                return HttpResponseRedirect("/product/index/")
            else:
                data[contenttype.ERROR] = "username or password error!"
    return render_to_response('user/login.html', data, RequestContext(request))


def query_index(query_dict, data):
    '''
    index界面搜索方法,并防止数据库注入
    param query_dict: 搜索的参数
    param data: 数据库查询结果
    '''
    keys = ("id", "gc_name", "goods_name")
    for index in query_dict:
        if index in keys and len(query_dict[index]) != 0:
            param = {index: query_dict[index]}
            data = data.filter(**param)
    return data


class UserControll(View):
    def index(self, request):
        if request.method == "GET":
            data = User.objects.all()
            try:
                data = query_index(request.GET, data)
            except ValueError:
                raise Http404
            paginator = Paginator(data, 25)
            page = request.GET.get("page")
            try:
                users = paginator.page(page)
            except PageNotAnInteger:
                users = paginator.page(1)
            except EmptyPage:
                users = paginator.page(paginator.num_pages)

            return HttpResponse(index_template.render(RequestContext(request, {"users": users})))

    def create(self, request):
        if request.method == "GET":
            permision = Group.objects.all()
            return render_to_response("user/edit.html", {"url": "/user/create/", "permision_group": permision},
                                      RequestContext(request))
        if request.method == "POST":
            params = request.POST
            user = User.create_user(**params)
            user.set_goups(params.get("permision_group"))
            return HttpResponseRedirect("/user/login")

    def update(self, request, id):
        if request.method == "GET":
            permision = Group.objects.all()
            user = User.objects.get(id=id)
            return render_to_response("user/edit.html",
                                      {"url": "/user/create/", "permision_group": permision, "user": user},
                                      RequestContext(request))


def logout(request):
    from django.contrib.auth import logout

    logout(request)
    return HttpResponseRedirect("/user/login")


class Userdetail(DetailView):
    '''
    用户信息
    '''
    model = User
    template_name = 'user/detail.html'

    def get(self, request, *args, **kwargs):
        return DetailView.get(self, request, *args, **kwargs)
