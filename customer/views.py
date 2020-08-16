from django.shortcuts import render, redirect
from django.http import HttpResponse
from management.models import *
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
import requests
from .models import Reservation as ReservationModel
import json

def Total(usr):
    dishes = Add_to_cart.objects.filter(user = usr)
    total = 0
    for i in dishes:
        total += (i.dish.price) * (i.qty)
    return dishes, total

def Home(request):
    if request.user.is_staff:
        return redirect('AdminHome')
    cat = Category.objects.all()
    dish = Dish.objects.filter(avail = True)
    if request.user.is_anonymous:
        d = {'cat':cat, 'dishes':dish}
    else:
        Cartdish, total = Total(request.user)
        d = {'cat':cat, 'dishes':dish, 'total':total, 'Cartdish':Cartdish}
    return render(request, 'index.html',d)

def Reservation(request):
    d = {}
    if request.POST:
        if not request.user.is_authenticated:
            return redirect('account')
        data = request.POST
        date = data['date']
        name = data['name']
        time = data['time']
        guests = data['guests']
        email = data['email']
        mob = data['mob']
        ReservationModel.objects.create(user = request.user, mob = mob, name = name, guests = guests, time = time, date = date)
    if request.user.is_authenticated:
        Cartdish, total = Total(request.user)
        d = {'total':total, 'Cartdish':Cartdish}
    return render(request,'reservation.html',d)

def Account(request):
    if request.user.is_authenticated:
        return redirect('home')
    errorLogin = False
    errorEmail = False
    errorPass = False
    errorUser = False
    if 'login' in request.POST:
        un = request.POST['un']
        pwd = request.POST['pwd']
        user = authenticate(username = un, password = pwd)
        if user:
            login(request, user)
            if request.user.is_staff:
                return redirect('AdminHome')
            else:
                return redirect('home')
        else:
            errorLogin = True
    if 'signup' in request.POST:
        e = request.POST['email']
        ev = json.loads(requests.get('https://api.trumail.io/v2/lookups/json?email='+e).text)
        un = request.POST['un']
        pwd1 = request.POST['pwd1']
        pwd2 = request.POST['pwd2']
        check = User.objects.filter(username = un)
        if (ev['validFormat'] is not True) or (ev['deliverable'] is not True):
            errorEmail = True
        elif pwd1 != pwd2:
            errorPass = True
        elif check:
            errorUser = True
        else:
            User.objects.create_user(username = un,email=e,password=pwd1, is_staff = False)
            user = authenticate(username = un, password = pwd1)
            login(request, user)
            return redirect('home')
        print('values = ',e,un,pwd1,pwd2)
    d = {'errorL':errorLogin, 'errorPass':errorPass, 'errorUser':errorUser, 'errorEmail':errorEmail}   
    return render(request, 'account.html',d)

def Logout(request):
    logout(request)
    return redirect('account')

def Cart(request):
    orders, total = Total(request.user)
    d = {'orders':orders, 'total':total}
    return render(request, 'shop_cart.html',d)

def DeleteOrder(request, Oid):
    Add_to_cart.objects.filter(id = Oid).delete()
    return redirect('cart')

