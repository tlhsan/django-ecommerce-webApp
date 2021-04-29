from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# customer model
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE, null= True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name

# product model
class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_digital = models.BooleanField(default=False, blank=True, null=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    # if there is no image, then the image would not have any url so,
    # if no image url, send a blank link to avoid error
    @property
    def imageUrl(self):
        try:
            url = self.image.url
        except: 
            url = ''
        return url

# order model
# description: here order is separated from orderItem because order is the card(all the orders)
# and an orderItem is an item inside the cart
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False, blank=True, null=True)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    # get the grand total for all the items
    @property
    def grandTotal(self):
        orderitems = self.orderitem_set.all()
        grandtotal = sum([item.getTotalPrice for item in orderitems])
        return grandtotal

    # get the total number of items(quantity)
    @property
    def totalItems(self):
        orderitems = self.orderitem_set.all()
        totalitems = sum([item.quantity for item in orderitems])
        return totalitems

    @property
    def shipping(self):
        shipping = False
        # get all the order items to check if there is any digital product
        orderItems = self.orderitem_set.all()
        for item in orderItems:
            if item.product.is_digital == False:
                shipping = True
        return shipping
    
# orderItem model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    # to get the total value of the (items*quantities)
    @property
    def getTotalPrice(self):
        total = self.product.price * self.quantity
        return total

# ShippingAddress model
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    prefecture = models.CharField(max_length=200, null=True)
    zip_code = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
