# coding=utf-8

from users.forms import UserLoginForm
from core import contenttype
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib import auth
import logging
from django.views.generic.detail import DetailView
from users.models import User
from django.http.response import HttpResponseRedirect

log = logging.getLogger("user.logger")
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


def create(request):
    if request.method == "GET":
        return render_to_response("user/edit.html", {"url": "/user/create/"}, RequestContext(request))
    if request.method == "POST":
        params = request.POST
        User.create_user(**params)
        return HttpResponseRedirect("/user/login")


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
