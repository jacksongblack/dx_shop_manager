# encoding=utf-8
from django.db import models

# Create your models here.
class GoodsClass(models.Model):
    gc_name = models.CharField(max_length=100)
    gc_parant_id = models.CharField(max_length=32)
    gc_sort = models.IntegerField()
    gc_show = models.SmallIntegerField()
    gc_index_show = models.SmallIntegerField()
    gc_parent_path = models.CharField(max_length=200)

    class Meta:
        db_table = "goods_class"


class Goods(models.Model):
    goods_name = models.CharField(max_length=50)
    gc = models.ForeignKey(GoodsClass)
    gc_name = models.CharField(max_length=100)
    goods_image1 = models.CharField(max_length=200)
    goods_image2 = models.CharField(max_length=200)
    goods_image3 = models.CharField(max_length=200)
    goods_image4 = models.CharField(max_length=200)
    goods_image5 = models.CharField(max_length=200)
    goods_image7 = models.CharField(max_length=200)
    goods_video = models.CharField(max_length=200)
    goods_tag = models.CharField(max_length=100)
    goods_price = models.DecimalField(max_digits=10, decimal_places=2)
    goods_store_price = models.DecimalField(max_digits=10, decimal_places=2)
    goods_serial = models.CharField(max_length=50)
    goods_show = models.SmallIntegerField(max_length=6)
    goods_click = models.IntegerField(max_length=11)
    goods_state = models.SmallIntegerField(max_length=6)
    goods_commend = models.SmallIntegerField(max_length=6)
    goods_add_time = models.DateTimeField()
    goods_keywords = models.CharField(max_length=255)
    goods_description = models.CharField(max_length=255)
    goods_body = models.TextField()
    goods_close_reason = models.CharField(max_length=255)
    goods_store_state = models.SmallIntegerField(6)
    commentnum = models.IntegerField(max_length=11)
    salenum = models.IntegerField(max_length=11)
    spec_goods_color = models.CharField(max_length=300)
    spec_name = models.CharField(max_length=300)

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
    def __string_to_dict(self):
        pass

    def __dict_to_string(self):
        pass


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
    goods = models.ForeignKey(Goods, related_name="storage_set")
    storage_num = models.IntegerField(max_length=11)
    sale_num = models.IntegerField(max_length=11)
    storage_lock = models.IntegerField(max_length=11)
    spec_goods_color = models.CharField(max_length=20)
    spec_name = models.CharField(max_length=30)
    goods_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "goods_storage"