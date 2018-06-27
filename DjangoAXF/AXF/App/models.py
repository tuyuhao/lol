from django.db import models


# 首页
class Main(models.Model):
    name = models.CharField(max_length=100)
    img = models.CharField(max_length=200)
    trackid = models.CharField(max_length=30)

    class Meta:
        abstract = True  # 抽象类，不让迁移成表


# 轮播
class MainWheel(Main):
    class Meta:
        db_table = 'axf_wheel'


# 导航
class MainNav(Main):
    class Meta:
        db_table = 'axf_nav'


# 必购
class MainMustBuy(Main):
    class Meta:
        db_table = 'axf_mustbuy'


# 便利店
class MainShop(Main):
    class Meta:
        db_table = 'axf_shop'


class MainShow(Main):
    categoryid = models.CharField(max_length=100)
    brandname = models.CharField(max_length=100)

    img1 = models.CharField(max_length=200)
    childcid1 = models.CharField(max_length=100)
    productid1 = models.CharField(max_length=100)
    longname1 = models.CharField(max_length=100)
    price1 = models.CharField(max_length=30)
    marketprice1 = models.CharField(max_length=30)

    img2 = models.CharField(max_length=200)
    childcid2 = models.CharField(max_length=100)
    productid2 = models.CharField(max_length=100)
    longname2 = models.CharField(max_length=100)
    price2 = models.CharField(max_length=30)
    marketprice2 = models.CharField(max_length=30)

    img3 = models.CharField(max_length=200)
    childcid3 = models.CharField(max_length=100)
    productid3 = models.CharField(max_length=100)
    longname3 = models.CharField(max_length=100)
    price3 = models.CharField(max_length=30)
    marketprice3 = models.CharField(max_length=30)

    class Meta:
        db_table = 'axf_mainshow'


# 闪购
# 主商品分类
class FoodType(models.Model):
    typeid = models.CharField(max_length=20)
    typename = models.CharField(max_length=50)
    childtypenames = models.CharField(max_length=200)
    typesort = models.IntegerField()

    class Meta:
        db_table = 'axf_foodtypes'


'''
insert into axf_goods(
    productid,productimg,productname,productlongname,isxf,pmdesc,
    specifics,price,marketprice,categoryid,childcid,childcidname,
    dealerid,storenums,productnum) 

    values(
    "11951","img.jpg","","乐吧薯片鲜虾味50.0g",0,0,
    "50g",2.00,2.500000,103541,103543,"膨化食品",
    "4858",200,4);
'''


class Goods(models.Model):
    productid = models.CharField(max_length=20)
    productimg = models.CharField(max_length=200)
    productname = models.CharField(max_length=200)
    productlongname = models.CharField(max_length=200)
    isxf = models.BooleanField(default=0)
    pmdesc = models.CharField(max_length=200)

    specifics = models.CharField(max_length=200)
    price = models.FloatField()
    marketprice = models.FloatField()
    categoryid = models.CharField(max_length=20)
    childcid = models.CharField(max_length=20)
    childcidname = models.CharField(max_length=20)

    dealerid = models.CharField(max_length=20)
    storenums = models.IntegerField(default=1)
    productnum = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_goods'


class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=50)
    email = models.EmailField()
    icon = models.ImageField()
    sex = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)


class CardModel(models.Model):
    user = models.ForeignKey(User)
    goods = models.ForeignKey(Goods)
    num = models.IntegerField(default=1)
    is_select = models.BooleanField(default=True)


# 订单
class OrderModel(models.Model):
    order_id = models.CharField(max_length=100, unique=True)
    order_create = models.DateTimeField(auto_now_add=True)
    order_price = models.FloatField(default=0)
    # 订单状态：0表示待付款，1表示待收货，2表示待评价，3表示交易完成
    order_status = models.CharField(max_length=20, default=0)
    user = models.ForeignKey(User)


# 订单商品表
class OrderGoodsModel(models.Model):
    goods = models.ForeignKey(Goods)
    order = models.ForeignKey(OrderModel)
    num = models.IntegerField(default=1)
    price = models.FloatField(default=0)


