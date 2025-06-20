from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Service, CartItem ,Order
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from django.http import JsonResponse
import json
from .forms import CustomerRegisterForm


def home(request):
    return render(request, 'home.html') 


def register(request):
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False  # Not admin
            user.save()
            return redirect('login')
    else:
        form = CustomerRegisterForm()
    return render(request, 'register.html', {'form': form})


    
def user_login(request):
    if request.user.is_authenticated:
        return redirect('products')
    
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('products')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


@login_required
def service_list(request):
    services = Service.objects.all()
    return render(request, 'service_list.html', {'services': services})


@login_required
def add_to_cart(request, item_type, item_id):
    if item_type == 'product':
        item = Product.objects.get(id=item_id)
    else:
        item = Service.objects.get(id=item_id)

    CartItem.objects.create(
        name=item.name,
        price=item.price,
        quantity=1,
    )
    return redirect('cart')


@login_required
def view_cart(request):
    items = CartItem.objects.all()
    total = sum([item.total_price() for item in items])
    return render(request, 'cart.html', {'items': items, 'total': total})



@csrf_exempt  # if using fetch POST without CSRF token
@login_required
def checkout_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            cart = data.get('cart', {})
            total = Decimal(str(data.get('total', 0)))

            Order.objects.create(
                customer=request.user,
                products=json.dumps(cart),
                total_price=total
            )

            return JsonResponse({'success': True, 'message': 'Order placed successfully'})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


@login_required
def my_orders(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    # Convert product JSON to Python dict for each order
    for order in orders:
        order.product_data = json.loads(order.products)
    return render(request, 'my_orders.html', {'orders': orders})