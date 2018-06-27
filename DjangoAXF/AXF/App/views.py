import uuid

from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from .models import *


# 首页
def home(request):
    # 轮播数据
    wheels = MainWheel.objects.all()
    # 顶部菜单数据
    navs = MainNav.objects.all()
    # 必购商品
    mustbuys = MainMustBuy.objects.all()
    # 便利店商品
    shops = MainShop.objects.all()
    shop0 = shops.first()
    shop1_2 = shops[1:3]
    shop3_6 = shops[3:7]
    shop7_10 = shops[7:11]
    #   主体数据
    mainshows = MainShow.objects.all()

    data = {
        'title': '首页',
        'wheels': wheels,
        'navs': navs,
        'mustbuys': mustbuys,
        'shop0': shop0,
        'shop1_2': shop1_2,
        'shop3_6': shop3_6,
        'shop7_10': shop7_10,
        'mainshows': mainshows,

    }
    return render(request, 'home/home.html', context=data)


# 闪购
def market(request):
    return redirect(reverse('axf:market_with_params', args=('104749', '0', '0')))


def market_with_params(request, typeid, cid, sort_id):
    # 主商品分类数据
    foodtypes = FoodType.objects.all()
    # 获取商品数据
    goods_list = Goods.objects.filter(categoryid=typeid)

    # 如果不是'全部类型'，则继续根据子分类cid进行筛选
    if cid != '0':
        goods_list = goods_list.filter(childcid=cid)

    # 获取当前主分类下的所有子分类
    all_child_type = []
    current_types = foodtypes.filter(typeid=typeid)
    if current_types.exists():
        current_type = current_types.first()
        childtypenames = current_type.childtypenames
        #    childtypenames= '全部分类:0#进口水果:103534#国产水果:103533'
        child_type_list = childtypenames.split('#')
        for s in child_type_list:
            l = s.split(':')
            all_child_type.append(l)
    # print(all_child_type)
    # [['全部分类', '0'], ['进口水果', '103534'], ['国产水果', '103533']]

    # 排序规则
    if sort_id == '0':  # 综合排序
        pass
    elif sort_id == '1':
        goods_list = goods_list.order_by('-productnum')  # 销量排序
    elif sort_id == '2':
        goods_list = goods_list.order_by('-price')  # 价格降序
    elif sort_id == '3':
        goods_list = goods_list.order_by('price')  # 价格升序

    data = {
        'title': '零食分类',
        'foodtypes': foodtypes,  # 所有分类数据
        'goods_list': goods_list,  # 当前分类下所有的商品
        'typeid': typeid,  # 当前的类型id
        'all_child_type': all_child_type,  # 当前主分类下的所有子分类数据
        'cid': cid  # 当前的子分类id
    }
    return render(request, 'market/market.html', data)


def taobao(request, name):
    i = 'https://s.taobao.com/search?q=' + name
    return redirect(i)


# 我的
def mine(request):
    data = {
        'title': '用户中心',
        'username': '',
        'icon': '',
    }
    # 从session中获取登录用户的id
    user_id = request.session.get('user_id', '')
    # 判断是否为登录状态
    if user_id:
        users = User.objects.filter(id=user_id)
        if users.exists():
            user = users.first()
            data['username'] = user.username
            if user.icon:
                data['icon'] = '/uploads/' + user.icon.url

    return render(request, 'mine/mine.html', data)


# 我的-注册
def register(request):
    data = {
        'status': '1',
        'msg': 'ok',
    }
    # POST
    if request.method == 'POST':
        # 获取浏览器表单提交的数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        icon = request.FILES.get('icon')

        # print(username)
        # print(password)
        # print(email)
        # print(icon)
        # print(icon.name)
        # print(type(icon))

        # 检测
        # 用户名是否长度大于6位
        if len(username) < 6:
            data['status'] = '0'
            data['msg'] = '用户名长度不能小于6位'

            return render(request, 'user/register.html', data)

        # 注册
        try:
            user = User()
            user.username = username
            user.password = password
            user.email = email
            user.icon = icon
            user.save()

            # 注册成功后，进入'我的'页面,并自动登录
            request.session['user_id'] = user.id
            return redirect(reverse('axf:mine'))

        except:
            data['status'] = -1
            data['msg'] = '注册失败'
            return render(request, 'user/register.html', data)

    # GET
    else:
        return render(request, 'user/register.html', data)


# 退出登录，注销
def logout(request):
    # 删除session
    request.session.flush()
    return redirect(reverse('axf:mine'))


# 检测用户名是否已存在
def check_username(request):
    data = {
        'status': 1,
        'msg': 'ok'
    }
    if request.method == 'GET':
        username = request.GET.get('username')
        users = User.objects.filter(username=username)

        if users.exists():
            data['status'] = 0
            data['msg'] = '用户名已存在'

    else:
        data['status'] = -1
        data['msg'] = '请求方式错误'

    # 返回Json数据
    return JsonResponse(data)


# 我的-登录
def login(request):
    data = {
        'status': 1,
        'msg': 'ok'
    }
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(password)
        # 直接匹配用户名和密码是否存在
        '''
                users = User.objects.filter(username=username, password=password)
                if users.exists():
                    # 保存session，保存登录状态
                    request.session['user_id'] = users.first().id
                    return redirect(reverse('axf:mine'))  # 登录成功 则重定向跳转到 我的 页面
        '''
        # 先验证是否存在匹配的用户，然后再验证密码
        users = User.objects.filter(username=username)
        if users.exists():
            user = users.first()
            if user.password == password:
                request.session['user_id'] = users.first().id
                return redirect(reverse('axf:mine'))

            else:
                # 密码错误
                data['status'] = 0
                data['msg'] = '密码输入不正确'

        else:  # 用户不存在
            data['status'] = -1
            data['msg'] = '用户不存在'

        return render(request, 'user/login.html', data)
    else:
        return render(request, 'user/login.html', data)


# 购物车
def cart(request):
    # 先检查是否登录了
    user_id = request.session.get('user_id', "")
    if not user_id:
        return redirect(reverse('axf:login'))

    # 获取数据库中购物车表中所有的用户
    carts = CardModel.objects.filter(user_id=user_id)

    data = {
        'title': '购物车',
        'carts': carts,
    }
    return render(request, 'cart/cart.html', data)


# 加入购物车
def add_to_cart(request):
    data = {
        'status': 1,
        'msg': 'ok',
    }
    # 先判断用户是否已经登录
    # 1.如果登录了，则加入购物车
    # 2.如果没有登录，则进入登录页面
    user_id = request.session.get('user_id', '')
    if not user_id:
        data['status'] = -1
        data['msg'] = '请先登录'

    else:
        if request.method == "GET":
            goods_id = request.GET.get('goodsid')
            num = request.GET.get('num')

            carts = CardModel.objects.filter(user_id=user_id, goods_id=goods_id)
            # 如果该用户存在相同的商品，则将该商品数量增加
            if carts.exists():
                cart = carts.first()
                cart.num += int(num)  # 数量增加
                cart.save()

            # 如果不存在相同商品，则添加一条购物车数据
            else:
                cart = CardModel()
                cart.user_id = user_id
                cart.goods_id = goods_id
                cart.num = num
                cart.save()

        else:
            data['status'] = 0
            data['msg'] = '请求方式错误'

    return JsonResponse(data)


# 购物车下面的数量增加
def add_num(request):
    data = {
        'status': 1,
        'msg': 'ok',
    }
    # 1.判断用户是否登录
    # 2.将当前用户对应的购物车商品数量+1
    # 3.将结果返回给浏览器端

    user_id = request.session.get('user_id', '')
    # 未登录
    if not user_id:
        data['status'] = -1
        data['msg'] = '请先登录'
    # 已登录
    else:
        if request.method == 'GET':
            cart_id = request.GET.get('cartid')
            cart = CardModel.objects.get(pk=cart_id)
            cart.num += 1
            cart.save()
            data['num'] = cart.num

        else:
            data['status'] = 0
            data['msg'] = '请求方式错误'

    return JsonResponse(data)


# 数量减少
def sub_num(request):

    data = {
        'status': 1,
        'msg': 'ok',
    }
    user_id = request.session.get('user_id', '')
    # 未登录
    if not user_id:
        data['status'] = -1
        data['msg'] = '请先登录'
    # 已登录
    else:
        if request.method == 'GET':
            cart_id = request.GET.get('cartid')
            print(cart_id)
            cart = CardModel.objects.get(pk=cart_id)

            # 数量-1,最小只能为1
            cart.num -= 1
            if cart.num < 1:
                cart.num = 1

            cart.save()
            data['num'] = cart.num

        else:
            data['status'] = 0
            data['msg'] = '请求方式错误'

    return JsonResponse(data)


# 勾选/取消勾选
def change_select_state(request):
    data = {
        'status': 1,
        'msg': 'ok',
    }
    user_id = request.session.get('user_id', '')
    # 未登录
    if not user_id:
        data['status'] = -1
        data['msg'] = '请先登录'
    # 已登录
    else:
        if request.method == 'GET':
            cart_id = request.GET.get('cartid')
            cart = CardModel.objects.get(pk=cart_id)
            cart.is_select = not cart.is_select
            cart.save()
            # 将最新的勾选状态返回
            data['select'] = cart.is_select

        else:
            data['status'] = 0
            data['msg'] = '请求方式错误'

    return JsonResponse(data)


# 删除
def cart_del_goods(request):
    data = {
        'status': 1,
        'msg': 'ok',
    }
    user_id = request.session.get('user_id', '')
    # 未登录
    if not user_id:
        data['status'] = -1
        data['msg'] = '请先登录'
    # 已登录
    else:
        if request.method == 'GET':
            cart_id = request.GET.get('cartid')
            CardModel.objects.filter(pk=cart_id).delete()

        else:
            data['status'] = 0
            data['msg'] = '请求方式错误'

    return JsonResponse(data)


# 全选/全不选
def cart_change_select(request):
    data = {
        'status': 1,
        'msg': 'ok',
    }
    user_id = request.session.get('user_id', '')
    # 未登录
    if not user_id:
        data['status'] = -1
        data['msg'] = '请先登录'
    # 已登录
    else:
        if request.method == 'GET':
            selects = request.GET.get('selects')
            select_list = selects.split('#')
            action = request.GET.get('action')

            # 全不选
            if action == 'unselect':
                CardModel.objects.filter(id__in=select_list).update(is_select=False)

            # 全选
            else:
                CardModel.objects.filter(id__in=select_list).update(is_select=True)

        else:
            data['status'] = 0
            data['msg'] = '请求方式错误'

    return JsonResponse(data)


# 生成订单
def generate_order(request):
    data = {
        'status': 1,
        'msg': 'ok',
    }
    # 检查是否已经登录
    user_id = request.session.get('user_id', '')
    if not user_id:
        data['status'] = -1
        data['msg'] = '请先登录'
    else:
        if request.method == 'GET':
            selects = request.GET.get('selects')
            select_list = selects.split('#')

            # 生成订单
            order = OrderModel()
            order.user_id = user_id
            order.order_id = str(uuid.uuid4())
            order.save()

            # 生成订单商品数据
            total = 0
            for cartid in select_list:
                cart = CardModel.objects.get(id=cartid)

                order_goods = OrderGoodsModel()
                order_goods.order_id = order.id
                order_goods.goods_id = cart.goods_id
                order_goods.num = cart.num
                order_goods.price = cart.goods.price
                order_goods.save()

                total += int(order_goods.num) * float(order_goods.price)

            # 订单总价
            order.order_price = total
            order.save()

            data['orderid'] = order.id

        else:
            data['status'] = 0
            data['msg'] = '请求方式错误'

    return JsonResponse(data)


# 订单页面
def order_info(request, order_id):
    order = OrderModel.objects.get(id=order_id)
    data = {
        'order': order,
    }
    return render(request, 'order/orderinfo.html', data)


# 改变订单状态
def change_order_status(request):
    data = {
        'status': 1,
        'msg': 'ok',
    }

    user_id = request.session.get('user_id', '')
    if not user_id:
        data['status'] = -1
        data['msg'] = '请先登录'

    else:
        if request.method == "GET":
            orderid = request.GET.get('orderid')
            status = request.GET.get('status')
            # 把订单状态改变
            order = OrderModel.objects.get()

        else:
            data['status'] = 0
            data['msg'] = '请求方式错误'
    return JsonResponse(data)


# 待付款
def order_wait_pay(request):
    # 获取待付款的订单信息
    orders = OrderModel.objects.filter(order_status='0')

    data = {
        'orders': orders,
    }
    return render(request, 'order/orderwaitpay.html', data)


# 待收货
def order_paid(request):
    # 获取待收货的订单信息
    orders = OrderModel.objects.filter(order_status='1')

    data = {
        'orders': orders,
    }
    return render(request, 'order/orderpaid.html', data)