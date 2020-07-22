from django.urls import path
from .views import *

app_name="core"

urlpatterns = [
    path("",Home_view.as_view(),name="home"),
    path("product/<pk>",Product_view.as_view(),name="product"),
    path("Order",Cart_controller.show,name="order"),
    path("chechout/",Checkout_view.as_view(),name="checkout"),
    path("payment/",Payment_view.as_view(),name="payment"),
    path("add-to-cart/<pk>",Cart_controller.add_to_cart,name="add_cart"),
    path("remove-from-cart/<pk>",Cart_controller.remove_from_cart,name="remove_cart"),
    path("add-cupon",AddCopon.as_view(),name="add_cupon"),

]
