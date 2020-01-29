from django.conf import settings
from django.db import models

Category_CHOICE = (
    ('s','shirt'),
    ('sw','sport wear'),
    ('ow','outwear'),
)

Label_CHOICE = (
    ('p','primary'),
    ('s','secondy'),
    ('d','danger'),
)

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True,null=True)
    category = models.CharField(choices=Category_CHOICE,max_length=2)
    label = models.CharField(choices=Label_CHOICE,max_length=1)
    description = models.CharField(max_length=400)
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
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username

    def total_price(self):
        m=0;
        for i in self.items.all():
            m+=i.total_price()
        return m;
