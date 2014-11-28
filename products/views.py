# encoding=utf-8
from django.template import loader
from django.views.generic.base import View
from django.template.context import RequestContext
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect, Http404
from products.models import Goods
from  image.image import Images
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
create_template = loader.get_template("products/edit.html")
index_template = loader.get_template("products/index.html")
show_template = loader.get_template("products/show.html")


class QueryTools(object):
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


class ProductController(View):
    def index(self, request):
        if request.method == "GET":
            data = Goods.objects.all()
            try:
                data = QueryTools().query_index(request.GET, data)
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

        if request.method == "GET":
            try:
                data = Goods.objects.get(id=id)
            except ValueError:
                raise Http404
            return HttpResponse(create_template.render(
                RequestContext(request, {"product": data, "url": "".join(("/product/update/", id,"/"))})))
        if request.method == "POST":
            print(request.FILES)
            for index in request.FILES:
                print(Images(request.FILES[index]).waterMark().save("waterMark"))
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
            return HttpResponse(create_template.render(RequestContext(request, {"url": "/product/update"})))
        elif request.method == "POST":

            for index in request.FILES:
                Images(request.FILES[index]).waterMark().resize().save()
        return HttpResponseRedirect("/product/index")
