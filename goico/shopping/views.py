from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Service, CartItem

def home(request):
    return render(request, 'home.html') 


def register(request):
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False  # Not admin
            user.save()
            messages.success(request, "Account created. You can now log in.")
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