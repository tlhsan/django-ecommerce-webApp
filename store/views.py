import json
from django.shortcuts import render
from .models import Product, Order, OrderItem
# for updating items
from django.http import JsonResponse
# Create your views here.

# view for store page
def storeView(request):
    customer = request.user.customer
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=customer, is_completed=False)
        items = order.orderitem_set.all()
        cartItemsValue = order.totalItems
    else:
        items = []
        order = {
            'totalItems':0,
            'grandTotal':0,
            'shipping': False
        }
        cartItemsValue = order['totalItems']
    products = Product.objects.all()
    context = {
        'products': products,
        'cartItemsValue': cartItemsValue,
    }
    return render(request, 'store/store.html', context)

# view for cart page
def cartView(request):
    customer = request.user.customer
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=customer, is_completed=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {
            'totalItems':0,
            'grandTotal':0,
        }
    context = {
        'items': items,
        'order': order,
    }
    return render(request, 'store/cart.html', context)

# view for checkout page
def checkoutView(request):
    customer = request.user.customer
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=customer, is_completed=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {
            'totalItems':0,
            'grandTotal':0,
            'shipping': False,
        }
    context = {
        'items': items,
        'order': order,
    }
    return render(request, 'store/checkout.html', context)

# view for update item
def updateItem(request):
    # for the time being this is only happening for the users who are logged in
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('The product id is:', productId)
    print('the action is: ', action)
    # since all users are now a customer, thanks to oneToOne field
    customer = request.user.customer
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer = customer, is_completed=False)
    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item has been updated', safe=False)