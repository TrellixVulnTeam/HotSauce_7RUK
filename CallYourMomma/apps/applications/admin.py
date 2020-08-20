from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Product, Purchase, User
# Register your models here.

admin.site.unregister(Group)
admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(User)
