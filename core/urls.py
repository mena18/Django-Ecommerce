from django.urls import path
from .views import *

app_name="core"

urlpatterns = [
    path("",home_view,name="home"),
    path("product/",product_view,name="product"),
    path("chechout/",chechout_view,name="checkout"),

]
