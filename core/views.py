from django.shortcuts import render,HttpResponse
from .models import Item,OrderItem,Order
# Create your views here.


def home_view(request):
    items = Item.objects.all()
    return render(request,"home-page.html",{'items':items});


def product_view(request):
    items = Item.objects.all()
    return render(request,"product-page.html",{'items':items});


def chechout_view(request):
    items = Item.objects.all()
    return render(request,"checkout-page.html",{'items':items});
