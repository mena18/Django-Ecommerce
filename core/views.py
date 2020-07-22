from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from .models import *
from django.views.generic import ListView,DetailView,View
from django.contrib import messages
from django.utils import timezone
from .forms import *
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


import stripe
stripe.api_key = settings.STRIPE_API_KEY
# `source` is obtained with Stripe.js; see https://stripe.com/docs/payments/accept-a-payment-charges#web-create-token

class Home_view(View):
    def get(self,*args,**kwargs): 
        
        category = self.request.GET.get('cat','all')
        search_res = self.request.GET.get('search')

        if(category!='all'):
            items = Item.objects.filter(category=category)

        elif(search_res):
            items = Item.objects.filter(title__icontains=search_res)
        else:
            items = Item.objects.all()

        categories = Category_CHOICE
        context={'items':items,"categories":categories,"current_cat":category}
        return render(self.request,"core/home.html",context)


class Product_view(View):
    def get(self,*args,**kwargs):
        item = get_object_or_404(Item,pk=kwargs['pk'])
        context={'item':item}
        if self.request.user.is_authenticated:
            order_item = OrderItem.objects.filter(user=self.request.user,ordered=False,item=item)
            if(order_item.exists()):
                context['selected']=True
        return render(self.request,"core/product.html",context)



class Checkout_view(LoginRequiredMixin,View):
    def empty(self,lis):
        for i in lis:
            if(i==''):return 1;
        return 0

    def get(self,*args,**kwargs):

        form = CheckoutForm()
        order = Order.objects.get(user=self.request.user, ordered=False)
        if(order.items.count()<1):
            messages.info(self.request,"your cart is empty")
            return redirect("/")
        context = {'form':form,'order':order};
        if(not order.cupon):
            context['promocode_form']=True
        return render(self.request,"core/checkout.html",context);

    def post(self,*args,**kwargs):

        form = CheckoutForm(self.request.POST or None)
        if not form.is_valid():
            messages.error(self.request,'Form is not valid')
            return redirect("core:checkout");

        order = Order.objects.get(user=self.request.user,ordered=False)

        street_address = form.cleaned_data.get('street_address')
        apartment_address = form.cleaned_data.get('apartment_address')
        country = form.cleaned_data.get('country')
        zip = form.cleaned_data.get('zip')
        same_billing_address = form.cleaned_data.get('same_billing_address')
        set_default_shipping = form.cleaned_data.get('set_default_shipping')
        payment_option = form.cleaned_data.get('payment_option')



        address=""
        if (same_billing_address):
            address = self.request.user.user_profile.address
        elif(self.empty([street_address,apartment_address,country,zip])):
            messages.warning(self.request,"Fill all fields")
        else:
            address = Address.objects.create(
                user=self.request.user,
                street_address=street_address,
                apartment_address=apartment_address,
                country=country,
                Zip=zip,
                )
        order.address = address
        order.save();

        if(set_default_shipping):
            userprofile = User_Profile.objects.get(user=self.request.user)
            userprofile.address=address
            userprofile.save()


        return redirect("core:payment");


class Payment_view(LoginRequiredMixin,View):
    #payment
    def get(self,*args,**kwargs):

        order = Order.objects.get(user=self.request.user,ordered=False)
        if(not order.address):
            messages.warning(self.request,"you don't have registerd address ")
            return redirect("core:checkout")
        context={'order':order}
        if(not order.cupon):
            context['promocode_form']=True
        return render(self.request,"core/payment.html",context)

    def post(self,*args,**kwargs):
        token = self.request.POST['stripeToken']
        order = Order.objects.get(user=self.request.user,ordered=False)
        total = order.total_price()

        if (not self.stripe_charge(total,token)):
            return redirect('/')

        order.ordered=True
        payment = Payment()
        payment.user = self.request.user
        payment.amount = total
        payment.stripe_charge_id = token
        payment.save()
        order.payment = payment;
        order.save()
        for item in order.items.all():
            item.ordered=True
            item.save()
        Order.objects.create(user=self.request.user)
        messages.success(self.request,"you successfuly make the order you will get your order soon")
        return redirect("core:home");



    def stripe_charge(self,total,token):
        try:
            stripe.Charge.create(
              amount=int(total*100),
              currency="usd",
              source=token,
              description="My First Test Charge (created for API docs)",
            )
            return 1
        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.warning(self.request, f"{err.get('message')}")
            return 0

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.warning(self.request, "Rate limit error")
            return 0

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            print(e)
            messages.warning(self.request, "Invalid parameters")
            return 0

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.warning(self.request, "Not authenticated")
            return 0

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.warning(self.request, "Network error")
            return 0

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.warning(
                self.request, "Something went wrong. You were not charged. Please try again.")
            return 0

        except Exception as e:
            # send an email to ourselves
            messages.warning(
                self.request, "A serious error occurred. We have been notifed.")
            return 0



class AddCopon(LoginRequiredMixin,View):
    def post(self,*args,**kwargs):
        code = self.request.POST['code']
        cupon = Cupon.objects.filter(code=code,valid=True)
        order = Order.objects.get(user=self.request.user,ordered=False)

        if(not cupon.exists()):
            messages.warning(self.request,"Cupon not valid")
            return redirect(self.request.POST.get('back','/'))
        cupon=cupon[0]
        user_cupon=""
        if(cupon.Global):
            user_cupon,created = User_cupon.objects.get_or_create(user=self.request.user,cupon=cupon)
            print("-------------------------\n\n")
            print(user_cupon)
            print("\n\n-------------------------")
        else:
            user_cupon = User_cupon.objects.filter(user=self.request.user,cupon=cupon)
            if(not user_cupon.exists()):
                messages.warning(self.request,"you don't have that cupon")
                return redirect(self.request.POST.get('back','/'))
            user_cupon = user_cupon[0]
            print("-------------------------\n\n")
            print(user_cupon)
            print("\n\n-------------------------")


        print("-------------------------\n\n")
        print(type(user_cupon))
        print(user_cupon)
        print("\n\n-------------------------")


        if(not user_cupon.usable()):
            messages.warning(self.request,"you can't use that cupon any more")
            return redirect(self.request.POST.get('back','/'))

        user_cupon.times_used+=1
        user_cupon.save()

        order.cupon = cupon
        order.save()

        messages.success(self.request,"you successfuly added the cupon you have "+str(user_cupon.times_left())+" Times left ")
        return redirect(self.request.POST.get('back','/'));



        # check if user had that cupon and can use it
        # check that order dossen't have any other cupon
        # add the cupon to the order

# i must come here and find better way to organize order_item ot Order
# because i don't want to add user and order in orderitem


class Cart_controller():

    @login_required
    def show(request):
        order =  Order.objects.filter(user=request.user, ordered=False)
        if(order.exists()):
            return render(request,"core/order_view.html",{'order':order[0],"range":range(30)})
        else:
            messages.error(request,"you don't have cart")
            return redirect("core:home");
    
    @login_required
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
                return redirect("core:order")
            else:
                cur_order.items.add(order_item)
                messages.success(request, "Item is added successfuly")
                return redirect("core:product",pk=pk)

        else:
            cur_order = Order.objects.create(user=request.user,ordered_date=timezone.now())
            cur_order.items.add(order_item)
            messages.success(request, "Item is added successfuly")
            return redirect("core:product",pk=pk)

    @login_required
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
                messages.success(request, "This item was removed from your cart.")
                return redirect("core:order")
            else:
                messages.error(request, "You don't even have that item")
                return redirect("core:product",pk=pk)
        else:
            messages.error(request,"you don't have active cart ")
            return redirect("core:product",pk=pk)
