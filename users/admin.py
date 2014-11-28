from django.contrib import admin
from users.models import User
from users.forms import UserAdmin
from django.contrib.auth.models import Permission

# Register your models here.
admin.site.register(User,UserAdmin)
admin.site.register(Permission)