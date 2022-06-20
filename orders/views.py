from ast import Pass
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from decimal import Decimal
from .models import Pizza, Sub, Pasta, Salad, DinnerPlatter
from django.db.models import Sum
from django.shortcuts import get_object_or_404

from orders.models import CartItem, OrderItem
from .forms import PizzaForm, SubForm, PastaForm, SaladForm, DinnerPlatterForm


# Create your views here.
def register(request):
    if request.method == "POST":
        first_name = request.POST['name']
        last_name = request.POST['lname']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        confirm = request.POST['confirm']

        if not username or not email or not password or not confirm or not first_name or not last_name or password != confirm:
            messages.success(request, "There was an error with your registration")
            return redirect('register')

        try:
            User.objects.create_user(username, email, password)
        except:
            return messages.success(request, "There was an error with your registration")
            return redirect('register')

        User.first_name = first_name
        User.last_name = last_name
        return redirect('signin')

    return render(request, 'orders/register.html')

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user  = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return messages.success(request, "There was an error with your Sign in")
            return redirect('signin')
    return render(request, 'orders/signin.html')   

def home(request):
    return render(request, 'orders/home.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You logged out succesfully!")
    return redirect("signin")

def menu(request):
    if request.user.is_authenticated:
        data = {
            'Pizza' : PizzaForm(),
            'Sub': SubForm(),
            'Pasta': PastaForm(),
            'Salad': SaladForm(),
            'DinnerPlatter': DinnerPlatterForm(),
        }

        cart_items = CartItem.objects.filter(user_id= request.user.id)

        context = {
            'data':data,
            'num_cart_items': cart_items.count()
        }
        return render(request, 'orders/menu.html', context)
    else:
        return redirect('login')

def obtener_precio(request):
    menu_item = request.GET.get('menu_item')
    price = "--.--"

    if menu_item == 'Pizza':
        style = request.GET.get('style')
        size = request.GET.get('size')
        num_toppings = request.GET.get('num_toppings')
        is_special = request.GET.get('is_special')

        if is_special == 'true':
            is_special = True
        else:
            is_special = False

        if style != "" and size != "" and num_toppings != "":
            if is_special:
                menu_pizza = Pizza.objects.get(style=style, size=size,is_special=is_special)  
            else:
                menu_pizza = Pizza.objects.get(style=style, size=size, num_toppings=num_toppings, is_special=is_special)
            price = menu_pizza.price

    elif menu_item == 'Sub':
            ingredients = request.GET.get('ingredients')
            size = request.GET.get('size')
            extras = request.GET.get('extras')
            menu_sub = Sub.objects.get(ingredients=ingredients, size=size)
            price = menu_sub.price + Decimal(0.50)*int(extras)
    elif menu_item == 'Pasta':
            style = request.GET.get('style')
            menu_pasta = Pasta.objects.get(style=style)
            price = menu_pasta.price
    elif menu_item == 'Salad':
            style = request.GET.get('style')
            menu_salad = Salad.objects.get(style=style)
            price = menu_salad.price
    elif menu_item == 'DinnerPlatter':
            style = request.GET.get('style')
            size = request.GET.get('size')
            if style != "" and size != "":
                menu_dinner_platter = DinnerPlatter.objects.get(style=style, size=size)
                price = menu_dinner_platter.price
    else:
            price ="--.--"
    data = {
            'price': price
        }
    return JsonResponse(data)

def cart(request):
    if request.method == "POST":
        if request.POST['menu_item'] == 'Pizza':
            form = PizzaForm(request.POST)

            if form.is_valid():
                form = form.cleaned_data

                menu = "Pizza"
                style = form['style']
                size = form['size']
                is_special = False
                if 'is_special' in request.POST:
                    is_special = True
                num_toppings = form['num_toppings']
                toppings_list = []
                for topping in form['toppings']:
                    toppings_list.append(str(topping))
                toppings = ", ".join(toppings_list)

                if is_special:
                    menu_pizza = Pizza.objects.get(style=style, size=size,is_special=is_special)
                else:
                   menu_pizza = Pizza.objects.get(style=style, size=size, num_toppings=num_toppings, is_special=is_special)

                price = menu_pizza.price
                print(price)

                order = CartItem(menu=menu, size=size, style=style, additional=toppings, is_special=is_special, user_id=request.user.id, price=price)
                order.save()

        elif request.POST['menu_item'] == 'Sub':
            form = SubForm(request.POST)
            if form.is_valid():
                form = form.cleaned_data  
                menu = 'Sub'
                ingredients = form['ingredients']
                size = form['size']
                extras_list = []
                added_cost = Decimal(0.00)
                for extra in form['extras']:
                    extras_list.append(str(extra))
                    added_cost += extra.added_cost

                extras = ", ".join(extras_list)

                menu_sub = Sub.objects.get(ingredients=ingredients, size=size)
                price = menu_sub.price + Decimal(added_cost)

                order = CartItem(menu=menu, size=size, style=ingredients, additional=extras, is_special=False, user_id=request.user.id, price=price)
                order.save()
            redirect('menu')
        elif request.POST['menu_item'] == 'Pasta':
            form = PastaForm(request.POST)
            if form.is_valid():
                form = form.cleaned_data
                menu = 'Pasta'
                style = form['style']
            
            menu_pasta = Pasta.objects.get(style=style)
            price = menu_pasta.price

            order = CartItem(menu=menu, style=style, user_id=request.user.id, price=price)
            order.save()
        elif request.POST['menu_item'] == 'Salad':
            form = SaladForm(request.POST)
            if form.is_valid():
                form = form.cleaned_data
                menu = 'Salad'
                style = form['style']

                menu_salad = Salad.objects.get(style=style)
                price = menu_salad.price

                order = CartItem(menu=menu, style=style, user_id=request.user.id, price=price)
                order.save()
        elif request.POST['menu_item'] == DinnerPlatter:
            form = DinnerPlatterForm(request.POST)
            if form.is_valid():
                form = form.cleaned_data
                menu = 'DinnerPlatter'
                style = form['style']
                size = form['size']

                menu_dinner_platter = DinnerPlatter.objects.get(style=style, size=size)
                price = menu_dinner_platter.price

                order = CartItem(menu=menu, style=style, size=size, user_id=request.user.id, price=price)
                order.save()
        else:
            print("Post error")
            redirect('menu')

        cart_items = CartItem.objects.filter(user_id= request.user.id)
        if cart_items:
            total_cost = Decimal(cart_items.aggregate(Sum('price'))['price__sum'])
        else:
            total_cost = 0
        
        context = {
            'car_items' : cart_items,
            'num_cart_items': cart_items.count(),
            'total_cost': total_cost
        }
        return render(request, 'orders/cart.html', context)
    else:

        cart_items = CartItem.objects.filter(user_id= request.user.id)
        if cart_items:
            total_cost = Decimal(cart_items.aggregate(Sum('price'))['price__sum'])
        else:
            total_cost = 0

        context = {
            'cart_items': cart_items,
            'num_cart_items': cart_items.count(),
            'total_cost': total_cost
        }
        return render(request, 'orders/cart.html', context)

def checkout(request):
    if request.method == "POST":
        cart_items = CartItem.objects.filter(user_id= request.user.id)

        for item in cart_items:
            menu = item.menu
            size = item.size
            style = item.style
            additional = item.additional
            is_special = item.is_special
            price = item.price
            user_id = item.user_id
            order = OrderItem(menu=menu, size=size, style=style, additional=additional, is_special=is_special, price=price, user_id=user_id)
            order.save()
            item.delete()

            all_order_items = OrderItem.objects.order_by('is_complete', 'created at')

            user_order_items = all_order_items.filter(user_id=request.user.id)
            cart_items = CartItem.objects.filter(user_id= request.user.id)

            context = {
                'cart_items': cart_items,
                'all_order_items': all_order_items,
                'user_order_items': user_order_items,
                'num_cart_items': cart_items.count(),
            }
            return render(request, 'orders/checkout.html', context)
        else:
            all_order_items = OrderItem.objects.order_by('is_complete', 'created at')

            user_order_items = all_order_items.filter(user_id=request.user.id)
            cart_items = CartItem.objects.filter(user_id= request.user.id)

            context = {
            'cart_items': cart_items,
            'all_order_items': all_order_items,
            'user_order_items': user_order_items,
            'num_cart_items': cart_items.count(),  
            }
            return render(request, 'orders/checkout.html', context)

def remove(request, cart_item_id):
    cart_item = CartItem.objects.filter(id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

def mark_complete(request, order_item_id):
    order_item = OrderItem.objects.filter(id=order_item_id)
    order_item.update(is_complete=True)
    return redirect('checkout')