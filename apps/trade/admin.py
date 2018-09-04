from django.contrib import admin
from trade.models import ShoppingCart, OrderInfo, OrderGoods

admin.site.register(ShoppingCart)
admin.site.register(OrderInfo)
admin.site.register(OrderGoods)
