from django.db import models


class GoodsClass(models.Model):
    gc_name = models.CharField(max_length=100)
    gc_parent = models.ForeignKey("self", null=True, blank=True, related_name="node")
    gc_sort = models.IntegerField(default=0)
    gc_show = models.SmallIntegerField(default=0)
    gc_index_show = models.SmallIntegerField(default=1)
    gc_parent_path = models.CharField(default="null", max_length=200)

    class Meta:
        db_table = "goods_class"

    def __str__(self):
        return self.gc_name

    @classmethod
    def create(cls, **params):
        keys = ("gc_name", "gc_sort", "gc_show", "gc_index_show", "gc_parent_path")
        category = {}
        for key in keys:
            if key in params.keys() and params.get(key):
                category[key] = params.get(key)[0]
        obejct = cls.objects.create(**category)
        params_get_parent_id = params.get("gc_parent_id")[0]
        if params_get_parent_id:
            cls.objects.get(id=params_get_parent_id).node.add(obejct)
        return obejct

# Create your models here.
