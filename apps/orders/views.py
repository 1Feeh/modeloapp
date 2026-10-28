from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from orders.models import Order
from orderitems.models import Orderitem
from products.models import Product
from clients.models import Client
from employees.models import Employee

# Create your views here.
def list_orders(request):
    template_name = 'orders/list_orders.html'
    orders = Order.objects.select_related('client', 'employee').all()
    context = {
        'orders': orders,
    }
    return render(request, template_name, context)


def list_items_products(request):
    template_name = 'orders/list_items_products.html'
    products = Product.objects.filter(is_active=True)
    context = {
        'products': products,
    }
    return render(request, template_name, context)


def cart(request):
    template_name = 'orders/cart.html'
    cart = request.session.get('cart', {})
    total = 0.0
    for key, item in cart.items():
        total += float(item['subtotal'])
    context = {
        'cart': cart,
        'total': total,
    }
    return render(request, template_name, context)


def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    pid = str(product.id)
    if pid in cart:
        cart[pid]['quantity'] += 1
    else:
        cart[pid] = {
            'name': product.name,
            'price': float(product.price),
            'quantity': 1,
            'subtotal': float(product.price),
        }
    quantity = cart[pid]['quantity']
    price = float(cart[pid]['price'])
    cart[pid]['subtotal'] = price * quantity
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('orders:cart')


def edit_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        pid = str(product_id)
        if pid in cart:
            if quantity <= 0:
                del cart[pid]
            else:
                price = float(cart[pid]['price'])
                cart[pid]['quantity'] = quantity
                cart[pid]['subtotal'] = price * quantity
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('orders:cart')


def delete_cart(request, product_id):
    cart = request.session.get('cart', {})
    pid = str(product_id)
    if pid in cart:
        del cart[pid]
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('orders:cart')


def checkout(request):
    template_name = 'orders/checkout.html'
    cart = request.session.get('cart', {})
    total = 0.0
    for key, item in cart.items():
        total += float(item['subtotal'])
    clients = Client.objects.all()
    employees = Employee.objects.all()
    if request.method == 'POST':
        client_id = request.POST.get('client')
        employee_id = request.POST.get('employee')
        payment_method = request.POST.get('payment_method')
        client = get_object_or_404(Client, id=client_id)
        employee = get_object_or_404(Employee, id=employee_id)
        order = Order.objects.create(
            client=client,
            employee=employee,
            payment_method=payment_method,
            status='Finalizado',
            total=0
        )
        total_order = 0.0
        for product_id, item in cart.items():
            product = get_object_or_404(Product, id=product_id)
            quantity = int(item['quantity'])
            unit_price = float(item['price'])
            subtotal = unit_price * quantity
            Orderitem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                unit_price=unit_price,
                subtotal=subtotal
            )
            total_order += subtotal
        order.total = total_order
        order.save()
        request.session['cart'] = {}
        request.session.modified = True
        return redirect('orders:view_order', order_id=order.id)
    context = {
        'cart': cart,
        'total': total,
        'clients': clients,
        'employees': employees,
        'payment_methods': Order._meta.get_field('payment_method').choices,
    }
    return render(request, template_name, context)


def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status != 'Cancelado':
        order.status = 'Cancelado'
        order.save()
    return redirect('orders:list_orders')


def view_order(request, order_id):
    template_name = 'orders/view_order.html'
    order = get_object_or_404(Order, id=order_id)
    items = order.items.all()
    context = {
        'order': order,
        'items': items,
    }
    return render(request, template_name, context)