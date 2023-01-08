from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from fexchange.settings import ROOT


class Fav(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=15)

class Pin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pin = models.CharField(max_length=6)

class PinVer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

class Currency(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100 ,verbose_name=" نام ارز")
    brand = models.CharField(max_length=100 ,null=True,verbose_name=" نماد ارز")
    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'currencies/{self.name}/'
    def get_image(self):
        return f'{ROOT}/media/{self.pic}'


class Wallet(models.Model):
    user = models.ForeignKey(User , related_name='wallets', on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency , related_name='wallets', on_delete=models.CASCADE)
    balance = models.FloatField(default= 0)
    
    def get_user(self):
        return self.user.username

    class Meta:
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'


class MainTrade(models.Model):
    name = models.CharField(max_length=100 ,verbose_name=" نام ارز")
    brand = models.CharField(max_length=100 ,null=True,verbose_name=" نماد ارز")
    scurrency = models.ForeignKey(Currency , related_name='sellcurrency', on_delete=models.CASCADE , null=True)
    bcurrency = models.ForeignKey(Currency , related_name='buycurrency' , on_delete=models.CASCADE , null=True)

    class Meta:
        verbose_name = 'MainTrade'
        verbose_name_plural = 'MainTrades'
        
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'{ROOT}/trades/{self.name}/'
    
    def get_bname(self):
        return self.bcurrency.name
    def get_sname(self):
        return self.scurrency.name


class Order(models.Model):
    currency = models.CharField(max_length=100)
    type = models.IntegerField()
    user = models.ForeignKey(User, related_name='maintradesellorders' , on_delete=models.CASCADE)
    amount = models.FloatField()
    price = models.FloatField()
    startamount = models.FloatField(null = True, blank = True)
    start = models.FloatField(null=True, blank = True)
    leverage = models.IntegerField(default= 0)
    tp = models.FloatField(null=True, blank = True)
    sl = models.FloatField(null=True, blank = True)
    limit = models.FloatField(null=True, blank = True)
    limit_amount = models.FloatField(null=True, blank = True)
    closed = models.BooleanField(default=True, null=True, blank = True)
    canceled = models.BooleanField(default=False)
    funding = models.FloatField(null=True, blank = True)
    date = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

class ClosedOrder(models.Model):
    currency = models.CharField(max_length=100)
    type = models.IntegerField()
    user = models.ForeignKey(User, related_name='his' , on_delete=models.CASCADE)
    amount = models.FloatField()
    price = models.FloatField()
    startprice = models.FloatField(null=True)
    leverage = models.IntegerField(default= 0)
    pnl = models.FloatField(null=True)
    fee = models.FloatField(null=True)
    funding = models.FloatField(null=True)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Close Order'
        verbose_name_plural = 'Close Orders'