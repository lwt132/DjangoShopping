from django.conf.urls import url
from django.contrib import admin

from app import views

urlpatterns = [
    url(r"^home/",views.home,name='home'),
    url(r"^market/$",views.market,name='market'),
    url(r"^market/(\d+)/(\d+)/(\d+)",views.marketSoft,name='marketSoft'),

    url(r"^cart/",views.cart,name='cart'),
    url(r"^mine/",views.mine,name='mine'),

    url(r"^register/",views.register,name='register'),
    # 3
    url(r"^checkUser/",views.checkUser,name='checkUser'),
    url(r"^loginUser/",views.loginUser,name='loginUser'),
    url(r"^logoutUser/",views.logoutUser,name='logoutUser'),
    # 4
    url(r"^addOrSubToCart/",views.addOrSubToCart,name='addOrSubToCart'),
    # 5
    url(r"^addOrSubCart/",views.addOrSubCart,name='addOrSubCart'),
    url(r"^cartGoodSelect/",views.cartGoodSelect,name='cartGoodSelect'),
    url(r"^cartAllSelect/",views.cartAllSelect,name='cartAllSelect'),

    url(r"^payPage/",views.payPage,name='payPage'),
    url(r"^payDeal/",views.payDeal,name='payDeal'),
    url(r"^goToPayStatusPage/",views.goToPayStatusPage,name='goToPayStatusPage'),
    url(r"^dealOrderPage/(\d)/",views.dealOrderPage,name='dealOrderPage'),

]