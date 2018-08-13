import hashlib
import time
import uuid
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
# Create your views here.
#主页
from django.urls import reverse
from app.models import HomeWheel, HomeNav, HomeMustBuy, HomeShop, HomeShow, LeftMenu, UserModel, CartMode, OrderModel, \
    OrderGoodModel
from app.models import  MarketGoods
def home(request):
    wheels = HomeWheel.objects.all()
    navs = HomeNav.objects.all()
    mustbuys = HomeMustBuy.objects.all()
    shops = HomeShop.objects.all()
    shop1 = shops[0:1]
    shop23 = shops[1:3]
    shop4567 = shops[3:7]
    shop891011 = shops[7:11]
    mainshows =HomeShow.objects.all()
    data = {
        "title": "主页",
        'wheels':wheels,
        'navs':navs,
        'mustbuys':mustbuys,
        "shop1":shop1,
        "shop23": shop23,
        "shop4567": shop4567,
        "shop891011": shop891011,
        "mainshows":mainshows,
    }
    return render(request,'home/home.html',context=data)
#商城
def market(request):
    return redirect(reverse('app:marketSoft',args=("104749","0","1")))

# 商城分类展示
def marketSoft(request,typeid,childcid,ranktype):
    foodsTypes = LeftMenu.objects.all()

    # MaGoods = MarketGoods.objects.all()  #所有商品
    if childcid == "0":
        MaGoods = MarketGoods.objects.filter(categoryid=typeid)
    else:
        MaGoods = MarketGoods.objects.filter(categoryid=typeid).filter(childcid=childcid)
    #选出子分类
    foodType = LeftMenu.objects.filter(typeid = typeid).first()
    childtypes = foodType.childtypenames.split("#")
    allchildTypes = []
    for childtype in childtypes:
        allchildTypes.append(childtype.split(":"))
    # print(allchildTypes)
    if ranktype == "1":
        pass
    elif ranktype == "2":
        MaGoods = MaGoods.order_by("productnum")
    elif ranktype == "3":
        MaGoods = MaGoods.order_by("price")
    elif ranktype == "4":
        MaGoods = MaGoods.order_by("-price")
    else:
        pass

    data = {
        "title":"商城",
        "foodstypes": foodsTypes,
        "Magoods": MaGoods,
        "typeid":typeid,
        "allchildTypes":allchildTypes,
        "childcid":childcid,
    }
    return render(request, 'market/market.html', context=data)

#购物车
def cart(request):
    userId = request.session.get("userId")
    users = UserModel.objects.filter(pk=userId)
    if not users.exists():
        return redirect(reverse("app:loginUser"))
    user = users.first()
    # user = UserModel()
    is_login = True
    AllSelect = True  #默认全选
    # 查询购物车数据
    cartDatas = CartMode.objects.filter(c_user=user)
    totalPrice = 0
    totalNum = 0
    haveGood = True
    if not cartDatas.exists(): #购物车没数据
        AllSelect = False
        haveGood = False
    else:
        for cart in cartDatas:
            if not cart.c_isselect:
                AllSelect = False

            if cart.c_isselect:
                num = float(cart.c_num)
                onePrice = float(cart.c_goods.price)
                goodprice = num * onePrice
                totalPrice += round(goodprice,2)
                totalNum += int(num)
        print(totalNum,totalPrice)
        print("------------------------------------")
    data = {
        "title": "购物车",
        "user": user,
        "is_login": is_login,
        "cartDatas":cartDatas,
        "AllSelect":AllSelect,
        "haveGood":haveGood,
        "totalNum":totalNum,
        "totalPrice":totalPrice,
    }
    return render(request,'cart/cart.html',context=data)
#我的
def mine(request):
    userId = request.session.get("userId")
    users = UserModel.objects.filter(pk=userId)
    if users.exists():  #存在用户
        user = users.first()
        # is_login = True
        imgPath = "/static/media/" + user.icon.url
        # user = UserModel()
        userOrders = user.ordermodel_set.all()
        nopayNum = 0
        waitReceiveNum = 0
        waitEvaluateNum = 0
        refundNum = 0
        for order in userOrders:
            if order.o_status == 1:
                nopayNum += 1
            if order.o_status == 2:
                waitReceiveNum += 1
            if order.o_status == 3:
                waitEvaluateNum += 1
            if order.o_status == 4:
                refundNum += 1
        print("---------------------------------------")
        print(nopayNum,waitReceiveNum,waitEvaluateNum,refundNum)
        data = {
            "title": "我的",
            "user":user,
            # "is_login":is_login,
            "imgPath":imgPath,
            "nopayNum":nopayNum,
            "waitReceiveNum":waitReceiveNum,
            "waitEvaluateNum":waitEvaluateNum,
            "refundNum":refundNum,
        }
        return render(request,'mine/mine.html',context=data)
    else:
        return redirect(reverse('app:loginUser'))

# 注册页面
def register(request):
    method = request.method
    if method == "GET":
        return  render(request, "user/user_register.html")
    elif method == "POST":
        # print("--------------1")
        username = request.POST.get("username")
        password = request.POST.get("password")
        # print(password)
        email = request.POST.get("email")
        icon = request.FILES["icon"]
        user = UserModel()
        user.username = username  #---------------------------------
        user.password = createPassword(password)
        user.email = email
        user.icon = icon
        user.save()
        request.session["userId"] = user.id
        return redirect(reverse("app:mine"))

# 服务器简单处理密码
def createPassword(password):
    mysha256 = hashlib.sha256()
    mysha256.update(password.encode("utf-8"))
    return mysha256.hexdigest()

# 检查用户名AJAXget请求
def checkUser(request):
    username = request.GET.get("username")
    res = UserModel.objects.filter(username=username)
    data = {}
    if res.exists():
        data["code"]="400"
        data["msg"]="不可用"
    else:
        data["code"]="200"
        data["msg"]="可用"
    return JsonResponse(data)

# 登录页面
def loginUser(request):
    method = request.method
    if method == "GET":
        return render(request, "user/user_login.html")
    if method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        # print(password)
        res = UserModel.objects.filter(username=username)
        if res.exists():
            user = res.first()
            if createPassword(password) == user.password:  #---------------------------------
                # 登陆成功设置session
                request.session["userId"] = user.id
                return redirect(reverse("app:mine"))
        return redirect(reverse("app:register"))

# 退出
def logoutUser(request):
    request.session.flush()
    return redirect(reverse("app:home"))

# 商城页面添加或减少购物车
def addOrSubToCart(request):
    userid = request.session.get("userId")
    res = UserModel.objects.filter(pk=userid)
    data = {}
    if not res.exists():  # 未登录
        data["code"] = "400"  # 未登录,重定向
        data["msg"] = "未登录,请重新登录"
        return JsonResponse(data)
    user = res.first()
    goodsid = request.GET.get("goodsid")
    action = request.GET.get("action")
    goods = MarketGoods.objects.filter(pk=goodsid).first() #获取商品
    cartGoods = CartMode.objects.filter(c_user=userid,c_goods=goodsid)
    if action == "add": #增加
        if cartGoods.exists():  # 存在该记录,表示修改
            cart = cartGoods.first()
            # cart = CartModel()
            cart.c_num += 1
            cart.save()
            data["num"] = cart.c_num
            data["code"] = "201"
        else:  # 不存在,则需要添加一条记录
            cart = CartMode()
            cart.c_goods = goods
            cart.c_user = user
            cart.c_num = 1
            cart.save()
            data["num"] = 1
            data["code"] = "202"

    if action == "sub": #减少
        cart = cartGoods.first()

        if cart.c_num == 1:
            cart.delete()
            data["code"] = "301"
        else:  #删除
            cart.c_num -= 1
            cart.save()
            data["num"] = cart.c_num
            data["code"] = "302"
    return JsonResponse(data)

# 购物车页面加减操作
def addOrSubCart(request):
    cartDataid = request.GET.get("cartDataid")
    action = request.GET.get("action")
    cartData = CartMode.objects.filter(pk=cartDataid).first()
    # cartData = CartMode()
    data = {}
    if action == "add":
        cartData.c_num += 1
        cartData.save()
        data["code"] = "201"
        data["num"] = cartData.c_num
    if action == "sub":
        if cartData.c_num == 1:
            cartData.delete()
            data["code"] = "302"
        if cartData.c_num > 1:
            cartData.c_num -= 1
            cartData.save()
            data["code"] = "301"
            data["num"] = cartData.c_num


    return JsonResponse(data)

# 购物车勾选
def cartGoodSelect(request):
    cartDataid = request.GET.get("cartDataid")
    cartData = CartMode.objects.filter(pk=cartDataid).first()
    # cartData = CartMode()
    cartData.c_isselect = (not cartData.c_isselect)
    cartData.save()
    data = {}
    data["code"] = "200"
    data["isselect"] = cartData.c_isselect
    return JsonResponse(data)

# 购物车点击全选
def cartAllSelect(request):
    data = {}
    cartIds = request.GET.get("cartids")
    action = request.GET.get("action")
    print(cartIds)
    print(action)
    cartIdList = cartIds.split("#")
    print(cartIdList)
    if action == "allSelectChange":  # 由全部选中变为全部不选中
        for id in cartIdList:
            cart = CartMode.objects.filter(pk=id).first()
            # cart = CartMode()
            cart.c_isselect = False
            cart.save()
        data["code"] = "201"
    if action == "noAllSelect":
        for id in cartIdList:
            cart = CartMode.objects.filter(pk=id).first()
            cart.c_isselect = True
            cart.save()
        data["code"] = "202"  #未全选中的部分变成全选中
    return JsonResponse(data)

# 支付页面
def payPage(request):
    data = {}
    userid = request.session.get("userId")
    user = UserModel.objects.filter(pk=userid).first()
    carts = CartMode.objects.filter(c_user=user)
    isSelectCart = []
    for cart in carts:
        if cart.c_isselect:
            isSelectCart.append(cart)
            cart.delete()
    if len(isSelectCart) == 0: #没有商品，先购买商品
        return redirect(reverse("app:market"))
    else:  #有商品，前往支付页面
        order = OrderModel()
        order.o_number = str(uuid.uuid4())  #订单号
        order.o_user = user
        order.o_status = 1 #未支付
        order.save()
        for cart in isSelectCart:
            orderGood = OrderGoodModel()
            orderGood.og_num = cart.c_num
            orderGood.og_good = cart.c_goods
            orderGood.og_order = order
            orderGood.save()
        data["orderGoods"] = OrderGoodModel.objects.filter(og_order=order) #订单商品
        data["orderNum"] = order.o_number
        return render(request,"buygoodsinfo/payPage.html",context=data)

# 支付处理
def payDeal(request):
    data = {}
    userid = request.session.get("userId")
    orderNum = request.GET.get("orderNum")
    goodsProductid = request.GET.get("goodsProductid").split("#")
    goodsnum = request.GET.get("goodsnum").split("#")
    print(goodsProductid)
    print(goodsnum)
    user = UserModel.objects.filter(pk=userid).first()
    # user = UserModel()
    # 得到用户订单
    order = user.ordermodel_set.filter(o_number=orderNum).first()
    totalPrice = 0
    for i in range(len(goodsProductid)):
        price = MarketGoods.objects.filter(productid=goodsProductid[i]).first().price
        num = float(goodsnum[i])
        goodPrice = price * num
        totalPrice += goodPrice
    data["totalPrice"] = totalPrice
    # order = OrderModel
    order.o_status = 2 #支付成功
    order.save()
    return JsonResponse(data)

#支付状态页面             #未加入
def goToPayStatusPage(request):
    data ={}
    time.sleep(1)
    return render(request,'buygoodsinfo/payStatusPage.html',context=data)

# 处理订单请求。。。。未支付，待收货，待评价，退款
def dealOrderPage(request,action):
    data={}
    userid = request.session.get("userId")
    user = UserModel.objects.filter(pk=userid).first()
    # user = UserModel()
    # print("------------------------------")
    # print(action)
    if action == "1":
        orders = user.ordermodel_set.filter(o_status=1)
        # print(111111111111111111111111111)
        if orders.exists():
            # print(222222222222222222222222222)
            data["orders"] = orders
            return render(request,"buygoodsinfo/nopayOrderPage.html",context=data)
        else:
            return redirect(reverse('app:mine'))
    elif action == "2":
        orders = user.ordermodel_set.filter(o_status=2)
        if orders.exists():
            data["orders"] = orders
            return render(request, "buygoodsinfo/waitReceiveOrderPage.html", context=data)
        else:
            return redirect(reverse('app:mine'))
    elif action == "3":
        orders = user.ordermodel_set.filter(o_status=3)
        if orders.exists():
            data["orders"] = orders
            return render(request, "buygoodsinfo/waitEvaluateOrderPage.html", context=data)
        else:
            return redirect(reverse('app:mine'))
    elif action == "4":
        orders = user.ordermodel_set.filter(o_status=4)
        if orders.exists():
            data["orders"] = orders
            return render(request, "buygoodsinfo/refundOrder.html", context=data)
        else:
            return redirect(reverse('app:mine'))
