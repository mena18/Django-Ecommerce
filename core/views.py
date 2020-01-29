from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from .models import Item,OrderItem,Order
from django.views.generic import ListView,DetailView,View
from django.contrib import messages
from django.utils import timezone
# Create your views here.

def chechout_view(request):
    items = Item.objects.all()
    return render(request,"core/checkout.html",{'items':items});


class Home_view(ListView):
    template_name = "core/home.html"
    model = Item
    context_object_name = 'items'

class Product_view(DetailView):
    template_name = "core/product.html"
    context_object_name = 'item'
    model = Item


class Order_view(View):
    def get(self,*args,**kwargs):
        order =  Order.objects.filter(user=self.request.user, ordered=False)
        if(order.exists()):
            return render(self.request,"core/order_view.html",{'order':order[0]})
        else:
            messages.error(self.request,"you don't have cart")
            return redirect("core:home");

# i must come here and find better way to organize order_item ot Order
# because i don't want to add user and order in orderitem
def add_to_cart(request,pk):
    item = get_object_or_404(Item,pk=pk)
    quantity = int(request.POST['quantity']);
    if(quantity<0):
        messages.error(request,"can't add negative quantity");
        return redirect("core:home");

    order_item,created = OrderItem.objects.get_or_create(
    item=item,
    user = request.user,
    ordered = False,
    )
    order_item.quantity = quantity;
    order_item.save()
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if(order_qs.exists()):
        cur_order = order_qs[0]
        if cur_order.items.filter(item__pk=pk).exists():
            messages.success(request, "This item quantity was updated.")
            return redirect("core:product",pk=pk)
        else:
            cur_order.items.add(order_item)
            messages.success(request, "Item is added successfuly")
            return redirect("core:product",pk=pk)

    else:
        cur_order = Order.objects.create(user=request.user,ordered_date=timezone.now())
        cur_order.items.add(order_item)
        messages.success(request, "Item is added successfuly")
        return redirect("core:product",pk=pk)


def remove_from_cart(request,pk):
    item = get_object_or_404(Item,pk=pk)

    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if(order_qs.exists()):
        order = order_qs[0]
        items = order.items.filter(item__pk=pk,user=request.user,ordered=False)
        if(items.exists()):
            item=items[0]
            order.items.remove(item)
            item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:product",pk=pk)
        else:
            messages.error(request, "You don't even have that item")
            return redirect("core:product",pk=pk)
    else:
        messages.error(request,"you don't have active cart ")
        return redirect("core:product",pk=pk)
