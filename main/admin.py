from django.contrib import admin
from .models import Currency, MainTrade, Wallet, Order, ClosedOrder, Fav

# Register your models here.
admin.site.register(Currency)
admin.site.register(MainTrade)
admin.site.register(Wallet)
admin.site.register(Order)
admin.site.register(ClosedOrder)
admin.site.register(Fav)