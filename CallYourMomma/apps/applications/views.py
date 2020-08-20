from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .models import *

import stripe

stripe.api_key = 'sk_test_DMbMQeBb7Odup2WPI34UgaWa00RB1g4q4n'


def index(request):
    thisuser = request.user

    return render(request, 'applications/index.html')


def buynow(request):
    products = Product.objects.all()
    return render(request, 'applications/buynow.html', {'products': products})


def cart(request):
    print("CART")
    if 'user_id' in request.session:
        cart = []
        total = 0
        print("inside id method")
        if 'cart' in request.session:
            print("inside cart method")
            for product_id in request.session['cart']:
                prod = Product.objects.get(id=product_id)
                cart.append(prod)
                print(prod)
                total += prod.price
        context = {
            'total': total,
            'prods': cart,
            "user": User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'applications/cart.html', context)

    if 'user_id' not in request.session:
        print ("cart")
        return render(request, 'applications/cart.html')




def addToCart(request, product_id):
    if 'cart' not in request.session:
        print("Creating a cart")
        request.session['cart'] = []
    else:
        print("In adding to cart route")
        prod = Product.objects.get(id=product_id)
        print(prod.product_name)
        print('*'*80)
        cart = request.session['cart']
        cart.append(product_id)
        request.session['cart'] = cart
        print()
        print(request.session['cart'])
    return redirect("/cart")


def delete_item(request, product_id):
    cart = request.session['cart']
    cart.remove(product_id)
    request.session['cart'] = cart
    return redirect("/cart")


def ourstory(request):
    return render(request, 'applications/ourstory.html')


def contactus(request):
    return render(request, 'applications/contactus.html')


def faq(request):
    return render(request, 'applications/faq.html')

def checkout(request):
    print("CART")
    if 'user_id' in request.session:
        cart = []
        total = 0
        print("inside id method")
        if 'cart' in request.session:
            print("inside cart method")
            for product_id in request.session['cart']:
                prod = Product.objects.get(id=product_id)
                cart.append(prod)
                print(prod)
                total += prod.price
        context = {
            'total': total,
            'prods': cart,
            "user": User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'applications/stripe.html', context)

    if 'user_id' not in request.session:
        print ("cart")
        return render(request, 'applications/stripe.html')


def login(request):
    errors = {}
    if request.method == "POST":
        other_user = User.objects.filter(email=request.POST['email'])
        try:
            this_user = other_user[0]
            print('this_user:')
            print(this_user.first_name)
            if request.POST['password'] == this_user.password:
                request.session['first_name'] = this_user.first_name
                user = User.objects.get(email=request.POST["email"]).id
                print(user)
                request.session['user_id'] = user
                return redirect("/")
            errors["password"] = "You forgot your password"
        except:
            errors['email'] = "No user exists here, go ahead and register"
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
    return render(request, "applications/login.html")


def register(request):
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/register')
        else:
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            email = request.POST["email"]
            password = request.POST["password"]
            user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=password)
            messages.success(request, "You have been logged out")
            request.session['user_id'] = user.id
            return redirect('/login')
    return render(request, "applications/register.html")
    


def logout(request):
    request.session.clear()
    return redirect("/")


def charge(request):

    if request.method == "POST":
        print('Data:', request.POST)
        amount = int(float(request.POST['amount']))
        customer = stripe.Customer.create(
            email=request.POST['email'],
            name=request.POST['name'],
            source=request.POST['stripeToken']
        )
        charge = stripe.Charge.create(
            customer=customer,
            amount= amount * 100,
            currency='usd',
            description="thanks",
        )
    return redirect(reverse('success', args=[amount]))


def successMsg(request, args):
    amount = args
    return render(request, 'applications/ordered.html', {'amount': amount})
