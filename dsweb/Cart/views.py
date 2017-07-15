# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from models import *
from django.db.models import Sum
from users.decorator import *
from users.models import *
def add(request):
    try:
        goodsid = int(request.GET.get('goodsid'))
        userid = request.session.get('uid')
        count = int(request.GET.get('count', '1'))

        carts = CartInfo.objects.filter(user_id = userid, goods_id = goodsid)
        if len(carts) >=1:
            cart = carts[0]
            cart.count += count
            cart.save()
        else:

            cart = CartInfo()
            cart.user_id = userid
            cart.goods_id = goodsid
            cart.count = count
            cart.save()
        return JsonResponse({'is_add': '1'})
    except:
        return JsonResponse({'is_add': '0'})

def count(request):
    uid = request.session.get('uid')
    # count = CartInfo.objects.filter(user_id=uid).count()
    count = CartInfo.objects.aggregate(Sum('count')).get('count__sum')

    return JsonResponse({'count':count})
@login_yz
def index(request):
    uid = request.session.get('uid')
    cart_list = CartInfo.objects.filter(user_id = uid,)
    context = {'title':'购物车','cart_list':cart_list}
    return render(request,'Cart/cart.html',context)

def save_count(request):
    try:
        id = request.GET.get('cartid')
        count = int(request.GET.get('count'))
        cart = CartInfo.objects.get(id= int(id))
        cart.count = count
        cart.save()
        return JsonResponse({'check':1})
    except:
        return JsonResponse({'check':0})


def delete(request):
    try:
        id = request.GET.get('id')
        cart = CartInfo.objects.get(pk=int(id))
        cart.delete()
        return JsonResponse({'check':1})
    except:
        return JsonResponse({'check':0})
@login_yz
def order(request):
    uid = request.session.get('uid')
    user = userinfo.objects.get(pk=int(uid))
    ids = request.POST.getlist('check_id')
    cart_ids = ','.join(ids)
    cart_list = CartInfo.objects.filter(id__in=ids)
    context = {'title':'订单中心','cart_list':cart_list,'user':user,'cart_ids':cart_ids}
    return render(request,'Cart/order.html',context)














