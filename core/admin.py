from django.contrib import admin
from .models import Item,OrderItem,Order,Cupon,Payment,User_cupon,Address,User_Profile
from django.urls import path
from django.template.response import TemplateResponse
# Register your models here.


class adminOrder(admin.ModelAdmin):
    list_display = ['user','total_price','ordered']


@admin.register(Item)
class admin_item(admin.ModelAdmin):
    list_display = ('title','price','discount_price','category')
    list_filter = ('title','category')
    search_fields = ('title','category')

# admin.site.register(Item)
admin.site.register(Order,adminOrder)
admin.site.register(OrderItem)
admin.site.register(Cupon)
admin.site.register(Payment)
admin.site.register(User_cupon)
admin.site.register(Address)
admin.site.register(User_Profile)
