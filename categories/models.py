from django.db import models


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

# Create your models here.
