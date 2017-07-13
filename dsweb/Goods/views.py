# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from django.core.paginator import Paginator
from django.http import HttpRequest
from haystack.generic_views import SearchView
from datetime import datetime


def index(request):
    # 查询产品的类型,最火的4个，最新的3个
    goodslist = []
    goodstype = TypeInfo.objects.all()
    for type in goodstype:
        newgoods = type.goodsinfo_set.order_by('-id')[0:4]
        hotgoods = type.goodsinfo_set.order_by('-gclick')[0:3]
        goodslist.append({'type': type, 'newgoods': newgoods, 'hotgoods': hotgoods})

    context = {'title': '首页', 'goodslist': goodslist, 'display': '1'}
    return render(request, 'Goods/index.html', context)


def list(request, listid, pageid):
    try:
        sort_num = request.COOKIES.get('sort_num', '1')
        price_num = request.COOKIES.get('pricesort', '5')
        type = TypeInfo.objects.get(pk=listid)
        new_list = type.goodsinfo_set.order_by('-id')[0:2]
        goods = type.goodsinfo_set.order_by('-id')
        goods_revert = type.goodsinfo_set.order_by('gprice')
        gdsprice = type.goodsinfo_set.order_by('-gprice')
        gdsclick = type.goodsinfo_set.order_by('-gclick')
        pgid = int(pageid)
        p = Paginator(goods, 3)
        pr = Paginator(goods_revert, 3)
        p1 = Paginator(gdsprice, 3)
        p2 = Paginator(gdsclick, 3)
        if pgid < 1:
            pgid = 1
        elif pgid > p.num_pages:
            pgid = p.num_pages
        page = p.page(pgid)
        page_revert = pr.page(pgid)
        page2 = p1.page(pgid)
        page3 = p2.page(pgid)
        context = {'title': '商品列表', 'display': '1', 'page': page, 'page_revert': page_revert, 'page2': page2,
                   'page3': page3, 'type': type, 'new': new_list, 'sort_num': sort_num, 'price_num': price_num}
        return render(request, 'Goods/list.html', context)
    except:
        return render(request, '404.html')


def detail(request, goodsid):
    try:
        comment_list = GoodsComment.objects.filter(com_type_id=int(goodsid))

        goods = GoodsInfo.objects.get(pk=int(goodsid))
        goods.gclick += 1
        goods.save()
        new = GoodsInfo.objects.all().order_by('-id')[0:2]
        context = {'goods': goods, 'new': new, 'title': '商品详细页', 'display': '1', 'gds_id': goodsid,
                   'comment_list': comment_list}
        response = render(request, 'Goods/detail.html', context)
        reviewids = request.COOKIES.get('review_id', '').rstrip(',')

        goods_ids = reviewids.split(',')  # ''.split(',') == ['']

        if goodsid in goods_ids:
            goods_ids.remove(goodsid)
        goods_ids.insert(0, goodsid)

        if len(goods_ids) > 5:
            goods_ids.pop()
        reviewids = ','.join(goods_ids)
        print reviewids
        response.set_cookie('review_id', reviewids, max_age=60 * 60 * 24 * 7)
        return response
    except:
        return render(request, '404.html')


def numbers(request):
    number1 = request.GET.get('num', '1')
    number2 = request.GET.get('num2', '5')
    response = JsonResponse({'number1': number1, 'num2': number2})
    response.set_cookie('sort_num', number1, max_age=24 * 7 * 60 * 60)
    response.set_cookie('pricesort', number2, max_age=24 * 7 * 60 * 60)
    return response


class MySearchView(SearchView):
    def get_context_data(self, *args, **kwargs):
        context = super(MySearchView, self).get_context_data(*args, **kwargs)
        context['display'] = '1'
        page_range = []
        page = context.get('page_obj')

        if page.paginator.num_pages < 5:
            page_range = page.paginator.page_range
        elif page.number <= 2:
            page_range = range(1, 6)
        elif page.number >= page.paginator.num_pages - 1:
            page_range = range(page.paginator.num_pages - 4, page.paginator.num_pages + 1)
        else:
            page_range = range(page.number - 2, page.number + 3)

        context['page_range'] = page_range
        return context


def comment(request):
    post = request.POST
    goodsid = post.get('gdsid')
    content = post.get('content')
    uid = request.session.get('uid')
    now_time = datetime.now()

    gdscomment = GoodsComment()
    gdscomment.com_user_id = int(uid)
    gdscomment.com_type_id = int(goodsid)
    gdscomment.com_date = now_time
    gdscomment.com_content = content
    gdscomment.save()

    goods = GoodsInfo.objects.get(pk=int(goodsid))
    new = GoodsInfo.objects.all().order_by('-id')[0:2]
    comment_list = GoodsComment.objects.filter(com_type_id=int(goodsid))
    context = {'goods': goods, 'new': new, 'title': '商品详细页', 'display': '1', 'gds_id': goodsid, 'content': content,
               'comment_list': comment_list}
    response = render(request, 'Goods/detail.html', context)

    return response


def thumb_up(request):
    try:
        commentid = request.GET.get('comid','')
        comment = GoodsComment.objects.get(id=int(commentid))
        comment.com_zan += 1
        comment.save()
        return JsonResponse({'check': 1})
    except:
        return JsonResponse({'check': 0})

















