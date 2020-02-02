from django.contrib import admin
from .models import Item,OrderItem,Order,Cupon,Payment,User_cupon,Address,User_Profile
# Register your models here.


class orderAdmin(admin.ModelAdmin):
    list_display=['user','ordered','total_price']

admin.site.register(Item)
admin.site.register(Order,orderAdmin)
admin.site.register(OrderItem)
admin.site.register(Cupon)
admin.site.register(Payment)
admin.site.register(User_cupon)
admin.site.register(Address)
admin.site.register(User_Profile)
