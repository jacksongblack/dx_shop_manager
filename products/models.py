# encoding=utf-8
from django.db import models

# Create your models here.
class GoodsClass(models.Model):
    gc_name = models.CharField(max_length=100)
    gc_parent_id = models.CharField(default="nul", max_length=32)
    gc_sort = models.IntegerField(default=0)
    gc_show = models.SmallIntegerField(default=0)
    gc_index_show = models.SmallIntegerField(default=1)
    gc_parent_path = models.CharField(default="null", max_length=200)

    class Meta:
        db_table = "goods_class"

    @classmethod
    def create(cls, **params):
        keys = ("gc_name", "gc_parent_id", "gc_sort", "gc_show", "gc_index_show", "gc_parent_path")
        category = {}
        for key in keys:
            if key in params.keys():
                category[key] = params.get(key)[0]
        return cls.objects.create(**category)


class Warehouse(models.Model):
    '''
    库存
    '''
    # area = models.ForeignKey(DictCode)
    area_info = models.CharField(max_length=100)
    warehouse_name = models.CharField(max_length=100)
    warehouse_address = models.CharField(max_length=100)
    linkman = models.CharField(max_length=50)
    linkman_phone = models.CharField(max_length=11)
    longitude = models.DecimalField(max_digits=20, decimal_places=12)
    latitude = models.DecimalField(max_digits=20, decimal_places=12)
    status = models.SmallIntegerField(default=1)

    def __unicode__(self):
        return self.warehouse_name + '|' + self.area_info

    class Meta:
        db_table = 'warehouse'


class GoodsStorage(models.Model):
    warehouse = models.ForeignKey(Warehouse)
    goods = models.ForeignKey("Goods", related_name="storage_set")
    storage_num = models.IntegerField(max_length=11)
    sale_num = models.IntegerField(max_length=11)
    storage_lock = models.IntegerField(max_length=11)
    spec_goods_color = models.CharField(max_length=20)
    spec_name = models.CharField(max_length=30)
    goods_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "goods_storage"


def get_params(request):
    from plugin.image import Images

    image_key = ("goods_image1", "goods_image2", "goods_image3", "goods_image4", "goods_image5")
    keys = (
        "goods_store_price", "goods_show", "gc_id", "goods_name", "goods_body", "goods_price", "goods_story_price",
        "goods_body")
    params_dict = {}
    for image_index in image_key:
        if image_index in request.FILES.keys():
            params_dict[image_index] = Images(request.FILES[image_index]).waterMark().save()["waterMark"]
    for key in keys:
        if key in request.POST.keys():
            params_dict[key] = request.POST[key]

    print(params_dict)
    return params_dict


class Goods(models.Model):
    goods_name = models.CharField(max_length=50)
    gc = models.ForeignKey(GoodsClass)
    gc_name = models.CharField(max_length=100)
    goods_image1 = models.CharField(max_length=200, null=True, blank=True)
    goods_image2 = models.CharField(max_length=200, null=True, blank=True)
    goods_image3 = models.CharField(max_length=200, null=True, blank=True)
    goods_image4 = models.CharField(max_length=200, null=True, blank=True)
    goods_image5 = models.CharField(max_length=200, null=True, blank=True)
    goods_image7 = models.CharField(max_length=200, blank=True)
    goods_video = models.CharField(max_length=200, blank=True)
    goods_tag = models.CharField(max_length=100, blank=True)
    goods_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    goods_store_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    goods_serial = models.CharField(default=0, max_length=50, blank=True)
    goods_show = models.SmallIntegerField(default=1, max_length=6)
    goods_click = models.IntegerField(default=1, max_length=11, blank=True, null=True)
    goods_state = models.SmallIntegerField(default=1, max_length=6, null=False)
    goods_commend = models.SmallIntegerField(default=1, max_length=6, null=False)
    goods_add_time = models.DateTimeField(null=False)
    goods_keywords = models.CharField(max_length=255, null=True)
    goods_description = models.CharField(max_length=255, null=True)
    goods_body = models.TextField(null=True)
    goods_close_reason = models.CharField(max_length=255, null=True)
    goods_store_state = models.SmallIntegerField(6, null=True)
    commentnum = models.IntegerField(default=1, max_length=11, null=True)
    salenum = models.IntegerField(default=1, max_length=11, null=True)
    spec_goods_color = models.CharField(max_length=300, null=True)
    spec_name = models.CharField(max_length=300, null=True)

    class Meta:
        db_table = "goods"

    def get_stock_number(self):
        num = 0
        for storage in self.storage_set.all():
            num += int(storage.storage_num)
        return num

    def get_sale_number(self):
        num = 0
        for storage in self.storage_set.all():
            num += int(storage.sale_num)
        return num

    def update_object(self, request):
        params = get_params(request)
        for index in params.keys():
            setattr(self, index, params[index])
        return self

    def save(self, *args, **kwargs):
        import datetime

        if not self.id:
            self.goods_add_time = datetime.datetime.today()
        return super(Goods, self).save(*args, **kwargs)

    @classmethod
    def query_index(cls, query_dict):
        '''
        index界面搜索方法,并防止数据库注入
        param query_dict: 搜索的参数
        param data: 数据库查询结果
        '''
        query_keys = ("id", "gc_name", "goods_name")
        params = {}
        for key in query_dict:
            if key in query_keys and key in query_dict.keys() and len(query_dict[key][0]) != 0:
                params[key] = query_dict[key][0]
        if params:
            data = cls.objects.filter(**params)
        else:
            data = cls.objects.all()
        return data

    @classmethod
    def form_create(cls, request):
        params_dict = get_params(request)

        return cls.objects.create(**params_dict)





