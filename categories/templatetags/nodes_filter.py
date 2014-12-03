from django import template

register = template.Library()


@register.filter(name="get_nodes", )
def get_nodes_name(category):
    s = ""
    categories = category.node.all()
    for object in categories:
        s += ''.join(("<option>", object.gc_name.encode("utf-8"), "</option>"))
    return s