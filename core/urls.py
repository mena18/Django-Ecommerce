from django.urls import path
from .views import *

app_name="core"

urlpatterns = [
    path("",Home_view.as_view(),name="home"),
    path("product/<pk>",Product_view.as_view(),name="product"),
    path("Order",Order_view.as_view(),name="order"),
    path("chechout/",chechout_view,name="checkout"),
    path("add-to-cart/<pk>",add_to_cart,name="add_cart"),
    path("remove-from-cart/<pk>",remove_from_cart,name="remove_cart"),

]
