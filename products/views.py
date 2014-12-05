# encoding=utf-8
from django.template import loader
from django.views.generic.base import View
from django.template.context import RequestContext
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect, Http404
from products.models import Goods, GoodsClass

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from plugin.cache import CacheFactory

# Create your views here.
create_template = loader.get_template("products/edit.html")
index_template = loader.get_template("products/index.html")
show_template = loader.get_template("products/show.html")


class ProductController(View):
    @method_decorator(permission_required("products.producs_index", login_url="/user/login"))
    def index(self, request):
        if request.method == "GET":
            data = CacheFactory().index_cache(request,Goods.query_index)
            paginator = Paginator(data, 25)
            page = request.GET.get("page")
            try:
                products = paginator.page(page)
            except PageNotAnInteger:
                products = paginator.page(1)
            except EmptyPage:
                products = paginator.page(paginator.num_pages)

            return HttpResponse(index_template.render(RequestContext(request, {"products": products})))

    @method_decorator(permission_required("products.producs_update", login_url="/user/login"))
    def update(self, request, id):
        try:
            data = Goods.objects.get(id=id)
        except ValueError:
            raise Http404
        if request.method == "GET":
            goods_class_objects_all = GoodsClass.objects.all()
            return HttpResponse(create_template.render(
                RequestContext(request, {"product": data, "goods_class": goods_class_objects_all,
                                         "url": "".join(("/product/update/", id, "/"))})))
        if request.method == "POST":
            data.update_object(request)
            data.save()
        return HttpResponseRedirect("/product/index")

    @method_decorator(permission_required("products.producs_show", login_url="/user/login"))
    def show(self, request, id):
        if request.method == "GET":
            try:
                data = Goods.objects.get(id=id)
            except :

                raise Http404

        return HttpResponse(show_template.render(RequestContext(request, {"product": data})))

    @method_decorator(permission_required("products.producs_delete", login_url="/user/login"))
    def delete(self, request, id):
        if request.method == "GET":
            data = Goods.objects.get(id=id)
            data.delete()
        return HttpResponseRedirect("/product/index")

    @method_decorator(permission_required("products.producs_create", login_url="/user/login"))
    def create(self, request):
        if request.method == "GET":
            goods_class_objects_all = GoodsClass.objects.all()
            return HttpResponse(create_template.render(
                RequestContext(request, {"goods_class": goods_class_objects_all, "url": "/product/create/"})))
        elif request.method == "POST":
            product = Goods.form_create(request)
            product.save()
        return HttpResponseRedirect("/product/index")
