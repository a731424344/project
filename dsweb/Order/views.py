from django.shortcuts import render, redirect
from django.db import transaction
# Create your views here.
from models import *
from datetime import datetime
from Cart.models import CartInfo


@transaction.atomic
def do_order(request):
    check = True
    sid = transaction.savepoint()
    try:
        uid = request.session.get('uid')
        time = datetime.now().strftime('%Y%m%d%H%M%S')
        main = OrderMain()
        main.order_id = '%s%d'%(time, uid)
        main.user_id = uid
        main.save()
        cartid_list = request.POST.get('cart_ids').split(',')
        print cartid_list
        carts = CartInfo.objects.filter(id__in=cartid_list)
        total = 0
        for cart in carts:
            if cart.count <= cart.goods.grepertory:
                detail = OrderDetail()
                detail.order = main
                detail.goods = cart.goods
                detail.price = cart.goods.gprice
                detail.count = cart.count
                detail.save()
                cart.goods.grepertory -= cart.count
                cart.goods.save()
                total += cart.goods.gprice * cart.count
                main.total = total
                main.save()
                cart.delete()
                check = True
            else:
                check = False
                transaction.savepoint_rollback(sid)
                break
        if check:
            transaction.savepoint_commit(sid)
    except:
        transaction.savepoint_rollback(sid)
        check = False
    finally:

        if check:
            return redirect('/order/')
        else:
            return redirect('/cart/')
