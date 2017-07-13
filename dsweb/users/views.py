# -*- coding:utf-8 -*-
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from PIL import Image, ImageDraw, ImageFont
import math,string
from models import *
from redis import StrictRedis
from hashlib import sha1
import datetime
from decorator import *
from Goods.models import *
def register(request):
    return render(request, 'users/register.html', {'title': '注册', 'top': '0'})


def login(request):
    uname = request.COOKIES.get('uname', '')

    return render(request, 'users/login.html', {'title': '登录', 'uname': uname, 'top': '0'})


def verify_code(request):

    # 引入随机函数模块
    import random
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    # str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码

    # val = random.randint(0x4E00, 0x9FBF)
    # str1 = unichr(val)
    # head = random.randint(0xB0, 0xCF)
    # body = random.randint(0xA, 0xF)
    # tail = random.randint(0, 0xF)
    # val = (head << 8) | (body << 4) | tail
    # str1 = "%x" % val
    # val = random.randint(0xB0A0, 0xD0D0)
    # str1 = "%x"%val
    rand_str = ''
    for i in range(0,4):
        head = random.randint(0xB0, 0xCF)
        body = random.randint(0xA, 0xF)
        tail = random.randint(0, 0xF)
        val = (head << 8) | (body << 4) | tail
        str1 = "%x" % val
        rand_str += str1.decode('hex').decode('gb2312')


    # for i in range(0, 4):
    #     rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    # font = ImageFont.truetype('FreeMono.ttf', 23)
    font = ImageFont.truetype('simsun.ttf', 16)

    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str

    # print request.session['verifycode']
    # 内存文件操作
    import cStringIO
    buf = cStringIO.StringIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


def info_handle(request):
    post = request.POST
    user_name = post.get('user_name')
    user_pwd = post.get('user_pwd')
    user_email = post.get('user_email')
    s1 = sha1()
    s1.update(user_pwd)
    upwd = s1.hexdigest()
    user_info = userinfo()
    user_info.user_name = user_name
    user_info.user_pwd = upwd
    user_info.user_email = user_email
    user_info.save()

    return render(request, 'users/success_register.html')


def re_name(request):
    user_name = request.GET.get('user_name')
    x = userinfo.objects.filter(user_name=user_name).count()
    return JsonResponse({'valid': x})


def login_handle(request):
    post = request.POST
    log_name = post.get('user_name')
    login_pwd = post.get('user_pwd')
    log_yzm = post.get('yzm').upper()
    yzm = request.session['verifycode']
    log_rember = post.get('rember')
    # rember = post.get('rember')
    s1 = sha1()
    s1.update(login_pwd)
    log_pwd = s1.hexdigest()
    sr = StrictRedis()
    redis_pwd = sr.get(log_name)

    context = {'title': '登录', 'uname': log_name, 'upwd': login_pwd, 'top': '0'}
    user_name = userinfo.objects.filter(user_name=log_name)
    if yzm == log_yzm:
        if redis_pwd is None:
            print ('xxx')
            if len(user_name) == 0:
                context['name_error'] = '1'
                return render(request, 'users/login.html', context)

            else:
                if user_name[0].user_pwd == log_pwd:
                    sr.set(log_name, log_pwd)
                    request.session['uid'] = user_name[0].id
                    request.session['uname'] = log_name
                    request.session.set_expiry(0)
                    url = request.session.get('url_path','/goods/')
                    response = redirect(url)
                    if log_rember == '1':

                        response.set_cookie('uname', log_name,
                                            expires=datetime.datetime.now() + datetime.timedelta(days=7))

                    else:
                        response.set_cookie('uname', '', max_age=-1)
                    return response
                else:
                    context['pwd_error'] = '1'
                    return render(request, 'users/login.html', context)
        else:
            if log_pwd == redis_pwd:
                request.session['uid'] = user_name[0].id
                request.session['uname'] = log_name
                request.session.set_expiry(0)
                #logout会清除session；
                url = request.session.get('url_path','/goods/')
                response = redirect(url)
                if log_rember == '1':

                    response.set_cookie('uname', log_name, expires=datetime.datetime.now() + datetime.timedelta(days=7))
                else:
                    response.set_cookie('uname', '', max_age=-1)

                return response
            else:
                context['pwd_error'] = '1'
                return render(request, 'users/login.html', context)

    else:
        context['yzm_error'] = '1'
        return render(request, 'users/login.html', context)


def change_pwd(request):
    context = {'title': '修改密码'}
    return render(request, 'users/change_pwd.html', context)


def newpwd_handle(request):
    post = request.POST
    uname = post.get('uname')
    uemail = post.get('uemail')
    upwd = post.get('upwd')
    user = userinfo.objects.filter(user_name=uname)
    context = {'uname': uname, 'uemail': uemail, 'upwd': upwd}
    if len(user) == 0:
        context['name_error'] = '1'
        return render(request, 'users/change_pwd.html', context)
    else:
        if user[0].user_email == uemail:
            s1 = sha1()
            s1.update(upwd)
            pwd_sha1 = s1.hexdigest()
            user[0].user_pwd = pwd_sha1
            user[0].save()
            sr = StrictRedis()
            sr.set(uname, pwd_sha1)
            return render(request, 'users/change_succ.html')
        else:
            context['email_error'] = '1'
            return render(request, 'users/change_pwd.html', context)

@login_yz
def center(request):
    try:
        user = userinfo.objects.get(pk=request.session['uid'])
        reviews_id = request.COOKIES.get('review_id')
        reviews_id = reviews_id.rstrip(',').split(',')
        # print reviews_id
        gdslist = []
        for goods in reviews_id:
            gdslist.append(GoodsInfo.objects.get(id=goods))
        context = {'title': '用户中心', 'user': user,'review_list':gdslist}
        return render(request, 'users/user_center_info.html', context)
    except:
        return render(request, 'users/user_center_info.html')


@login_yz
def order(request):
    context = {'title': '用户订单'}
    return render(request, 'users/user_center_order.html', context)


@login_yz
def siteinfo(request):
    user = userinfo.objects.get(pk = request.session['uid'])
    print user
    if request.method == 'POST':
        post = request.POST
        user.post_code = post.get('postcode')
        user.recv_name= post.get('recv_name')
        user.user_phone = post.get('recvphone')
        user.user_addr = post.get('detail_addr')
        user.save()
    context = {'user': user}
    return render(request,'users/user_center_site.html',context)

def logout(request):
    request.session.flush()
    return redirect('/login/')


def islogin(request):
    is_login = 0
    if request.session.get('uid'):
         is_login = 1
    return JsonResponse({'islogin':is_login})


















