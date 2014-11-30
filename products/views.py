# encoding=utf-8
from django.template import loader
from django.views.generic.base import View
from django.template.context import RequestContext
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect, Http404
from products.models import Goods, GoodsClass
from plugin.image import Images
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
create_template = loader.get_template("products/edit.html")
index_template = loader.get_template("products/index.html")
show_template = loader.get_template("products/show.html")


class ProductTools(object):
    def query_index(self, query_dict, data):
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

    def product_param(self, request):
        image_key = ("goods_image1", "goods_image2", "goods_image3", "goods_image4", "goods_image5")
        keys = (
        "goods_store_price", "goods_show", "gc_id", "goods_name", "goods_body", "goods_price", "goods_story_price",
        "goods_body")
        file_dict = {}
        params_dict = {}
        try:
            for image_index in image_key:
                file_dict[image_index] = Images(request.FILES[image_index]).waterMark().save()["waterMark"]

            for key in keys:
                params_dict[key] = request.POST[key]
        except:
            pass
        return dict(file_dict.items() + params_dict.items())


class ProductController(View):
    def index(self, request):
        if request.method == "GET":
            data = Goods.objects.all()
            try:
                data = ProductTools().query_index(request.GET, data)
            except ValueError:
                raise Http404
            paginator = Paginator(data, 25)
            page = request.GET.get("page")
            try:
                products = paginator.page(page)
            except PageNotAnInteger:
                products = paginator.page(1)
            except EmptyPage:
                products = paginator.page(paginator.num_pages)

            return HttpResponse(index_template.render(RequestContext(request, {"products": products})))


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
            params = ProductTools().product_param(request)
            data.update_object(**params)
            data.save()
        return HttpResponseRedirect("/product/index")


    def show(self, request, id):
        if request.method == "GET":
            try:
                data = Goods.objects.get(id=id)
            except ValueError:

                raise Http404

        return HttpResponse(show_template.render(RequestContext(request, {"product": data})))


    def delete(self, request, id):
        if request.method == "GET":
            if request.method == "GET":
                data = Goods.objects.get(id=id)
                data.delete()

        return HttpResponseRedirect("/product/index")


    def create(self, request):
        if request.method == "GET":
            goods_class_objects_all = GoodsClass.objects.all()
            return HttpResponse(create_template.render(
                RequestContext(request, {"goods_class": goods_class_objects_all, "url": "/product/create/"})))
        elif request.method == "POST":
            param = ProductTools().product_param(request)
            product = Goods.objects.create(**param)
            product.save()
        return HttpResponseRedirect("/product/index")
