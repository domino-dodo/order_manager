from django.shortcuts import render, redirect
from .models import Order, Customer
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import logout
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.delete()
    messages.success(request, 'Order deleted successfully.')
    return redirect('order_list')

@login_required
def mark_delivered(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.status = 'delivered'
    order.save()
    messages.success(request, 'Order marked as delivered.')
    return redirect('order_list')

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # simple validation
        if password != confirm_password:
            return render(request, 'orders/register.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'orders/register.html', {'error': 'Username already exists'})

        user = User.objects.create_user(username=username, password=password)

        # auto login after register
        login(request, user)

        return redirect('order_list')

    return render(request, 'orders/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('order_list')
        else:
            return render(request, 'orders/login.html', {'error': 'Invalid credentials'})

    return render(request, 'orders/login.html')



@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    total_orders = orders.count()
    total_revenue = orders.filter(status='delivered').aggregate(Sum('price'))['price__sum'] or 0

    context = {
        'orders': orders,
        'total_orders': total_orders,
        'total_revenue': total_revenue
    }

    return render(request, 'orders/order_list.html', context)

@login_required
def add_order(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        product = request.POST.get('product')
        price = request.POST.get('price')

        customer, created = Customer.objects.get_or_create(
            name=name,
            phone=phone
        )

        Order.objects.create(
            user=request.user,  # 👈 IMPORTANT
            customer=customer,
            product_name=product,
            price=price
        )
        messages.success(request, 'Order added successfully.')
        return redirect('order_list')

    return render(request, 'orders/add_order.html')