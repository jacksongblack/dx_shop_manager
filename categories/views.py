# encoding=utf-8
from django.template import loader
from django.views.generic.base import View
from django.template.context import RequestContext
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect, Http404
from categories.models import GoodsClass

from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from plugin.cache import CacheFactory

# Create your views here.

categories_index_tempalte = loader.get_template("category/index.html")
category_edit_tempalte = loader.get_template("category/edit.html")
category_show_tempalte = loader.get_template("category/show.html")


class CategoriesController(View):
    @method_decorator(permission_required("categories.category_permissions", login_url="/user/login"))
    def index(self, request):
        data = CacheFactory().index_cache(request, GoodsClass.objects.filter, **{"gc_parent_id":None})
        return HttpResponse(categories_index_tempalte.render(RequestContext(request, {"categories": data})))

    @method_decorator(permission_required("categories.category_permissions", login_url="/user/login"))
    def create(self, request):
        if request.method == "GET":
            goods_class_objects_all = GoodsClass.objects.filter(gc_parent_id=None)
            return HttpResponse(category_edit_tempalte.render(
                RequestContext(request, {"categories": goods_class_objects_all, "url": "/categories/create/"})))
        elif request.method == "POST":
            params = dict(request.POST)
            product = GoodsClass.create(**params)
            product.save()
        return HttpResponseRedirect("/categories/index")

    @method_decorator(permission_required("categories.category_permissions", login_url="/user/login"))
    def delete(self, request, id):
        category = GoodsClass.objects.get(id=id)
        category.delete()
        return HttpResponseRedirect("/categories/index")
