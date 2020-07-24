from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone

Category_CHOICE = (
    ('s','shirt'),
    ('sw','sport wear'),
    ('ow','outwear'),
)

Label_CHOICE = (
    ('e','No Label'),
    ('p','new'),
    ('d','best seller'),
)

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True,null=True)
    category = models.CharField(choices=Category_CHOICE,max_length=2)
    label = models.CharField(choices=Label_CHOICE,max_length=1)
    description = models.CharField(max_length=400)
    extra_info = models.TextField(True,null=True)
    image = models.ImageField(upload_to="images")

    def __str__(self):
        return self.title

class OrderItem(models.Model):
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username+" Will buy "+str(self.quantity) +" OF "+ self.item.title

    def total_price(self):
        if(self.item.discount_price):
            return self.item.discount_price * self.quantity
        return self.quantity*self.item.price;


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    address = models.ForeignKey('Address',on_delete=models.SET_NULL,null=True,blank=True)
    payment = models.ForeignKey('Payment',on_delete=models.SET_NULL,null=True,blank=True)
    cupon = models.ForeignKey('Cupon',on_delete=models.SET_NULL,null=True,blank=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


    def cupon_discount(self):
        if(self.cupon):
            return self.actual_price()*(self.cupon.persent/100)
        return 0

    def actual_price(self):
        m=0;
        for i in self.items.all():
            m+=i.total_price()
        return m

    def total_price(self):
        return self.actual_price() - self.cupon_discount()


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    Zip = models.CharField(max_length=100)
    default = models.BooleanField(default=False)

    def __str__(self):
        return "{},{},{}".format(self.street_address,self.apartment_address,self.country)

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    stripe_charge_id = models.CharField(max_length=30,null=True,blank=True)
    paypal_charge_id = models.CharField(max_length=30,null=True,blank=True)

    def __str__(self):
        return "{} : ({})".format(self.user.username,self.amount)

class Cupon(models.Model):
    code = models.CharField(max_length=100)
    persent = models.IntegerField()
    num_times = models.IntegerField()
    valid = models.BooleanField(default=True)
    Global = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class User_cupon(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    cupon = models.ForeignKey("Cupon",on_delete=models.CASCADE)
    times_used = models.IntegerField(default=0)



    def usable(self):
        return self.times_used<self.cupon.num_times

    def times_left(self):
        return self.cupon.num_times - self.times_used

    def __str__(self):
        return self.user.username +" "+self.cupon.code


class User_Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    address = models.ForeignKey(Address,on_delete=models.CASCADE,null=True,blank=True)


def user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        order = Order.objects.create(user=instance)
        user_profile = User_Profile.objects.create(user=instance)


post_save.connect(user_receiver, sender=settings.AUTH_USER_MODEL)
