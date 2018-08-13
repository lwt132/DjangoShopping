from django.db import models

# Create your models here.
class Home(models.Model):
    img = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    trackid = models.CharField(max_length=16)
    class Meta:
        abstract = True
        db_table = 'axf_home'
#轮播图模型
class HomeWheel(Home):
    class Meta:
        db_table = "axf_wheel"
# 导航模型
class HomeNav(Home):
    class Meta:
        db_table = "axf_nav"
# 必买模型
class HomeMustBuy(Home):
    class Meta:
        db_table = "axf_mustbuy"
#购物模型
class HomeShop(Home):
    class Meta:
        db_table = "axf_shop"
#购物下三张图模型
class HomeShow(models.Model):
    trackid = models.CharField(max_length=10,default=0)
    name = models.CharField(max_length=100,default=0)
    img = models.CharField(max_length=200)
    categoryid = models.CharField(max_length=16)
    brandname = models.CharField(max_length=100)
    img1 = models.CharField(max_length=200)
    childcid1 = models.CharField(max_length=16)
    productid1 = models.CharField(max_length=16)
    longname1 = models.CharField(max_length=100)
    price1 = models.CharField(max_length=10)
    marketprice1 = models.CharField(max_length=10)

    img2 = models.CharField(max_length=200)
    childcid2 = models.CharField(max_length=16)
    productid2 = models.CharField(max_length=16)
    longname2 = models.CharField(max_length=100)
    price2 = models.CharField(max_length=10)
    marketprice2 = models.CharField(max_length=10)

    img3 = models.CharField(max_length=200)
    childcid3 = models.CharField(max_length=16)
    productid3 = models.CharField(max_length=16)
    longname3 = models.CharField(max_length=100)
    price3 = models.CharField(max_length=10)
    marketprice3 = models.CharField(max_length=10)

    class Meta:
        db_table = "axf_mainshow"

#-购物商城--左侧导航-----------------------------------
class LeftMenu(models.Model):
    typeid = models.CharField(max_length=10)
    typename = models.CharField(max_length=100)
    childtypenames = models.CharField(max_length=200)
    typesort =models.CharField(max_length=10)
    class Meta:
        db_table = "axf_foodtypes"
# 商品信息表
class MarketGoods(models.Model):
    productid = models.CharField(max_length=16)
    productimg = models.CharField(max_length=200)
    productname = models.CharField(max_length=100)
    productlongname = models.CharField(max_length=200)
    isxf = models.IntegerField(default=0)
    pmdesc = models.IntegerField(default=0)
    specifics = models.CharField(max_length=20)
    price = models.FloatField(default=0.0)
    marketprice = models.FloatField(default=0.0)
    categoryid = models.CharField(max_length=16)
    childcid = models.CharField(max_length=16)
    childcidname = models.CharField(max_length=100)
    dealerid = models.CharField(max_length=16)
    storenums = models.IntegerField(default=0)
    productnum = models.IntegerField(default=0)

    class Meta:
        db_table = "axf_goods"
# 用户表
class UserModel(models.Model):
    username = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=200,unique=True)
    sex = models.BooleanField(default=1)
    icon = models.ImageField(upload_to="icons")
    isdelete = models.BooleanField(default=0)
    class Meta:
        db_table = "axf_usermodel"

# 用户购物车表
class CartMode(models.Model):
    c_user = models.ForeignKey(UserModel)
    c_goods = models.ForeignKey(MarketGoods)
    c_num = models.IntegerField(default=1)
    c_isselect = models.BooleanField(default=1)
    class Meta:
        db_table = "axf_cartmodel"

# 订单表
class OrderModel(models.Model):
    o_number = models.CharField(max_length=64)
    o_user = models.ForeignKey(UserModel)
    o_data = models.DateTimeField(auto_now=True)
    o_status = models.IntegerField(default=0)
    class Meta:
        db_table="axf_ordermodel"


# # 订单商品表
class OrderGoodModel(models.Model):
    og_order = models.ForeignKey(OrderModel)
    og_good = models.ForeignKey(MarketGoods)
    og_num = models.IntegerField(default=1)
    class Meta:
        db_table = "axf_ordergoodmodel"