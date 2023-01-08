from django.shortcuts import render
from rest_framework.views import APIView 
from .serializers import OrderSerializer, WalletSerializer, UserSerializer, CloseOrderSerializer
from .models import Wallet, Currency, Order, Pin, PinVer, ClosedOrder, Fav
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import authentication
from django.contrib.auth.hashers import make_password
import requests
import json
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
# Create your views here.

class deposit(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        wallet = Wallet.objects.get(user = request.user, currency= Currency.objects.get(brand = 'USDT'))
        wallet.balance = wallet.balance + float(request.data['amount'])
        wallet.save()
        query = Wallet.objects.filter(user = request.user)
        serializer = WalletSerializer(query, many = True)
        return Response(serializer.data)

class withdraw(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        wallet = Wallet.objects.get(user = request.user, currency= Currency.objects.get(brand = 'USDT'))
        if wallet.balance > float(request.data['amount']):
            wallet.balance = wallet.balance - float(request.data['amount'])
            wallet.save()
        else:
            wallet.balance = 0
            wallet.save()
        query = Wallet.objects.filter(user = request.user)
        serializer = WalletSerializer(query, many = True)
        return Response(serializer.data)

class fav(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = Fav.objects.filter(user = request.user)
        list = []
        for item in query:
            list.append(item.symbol)
        return Response(list,status= status.HTTP_200_OK)

    def post(self, request):
        if not len(Fav.objects.filter(user = request.user, symbol = request.data['symbol'])):
            f = Fav(user = request.user, symbol = request.data['symbol'])
            f.save()
        else:
            Fav.objects.get(user = request.user, symbol = request.data['symbol']).delete()
            
        query = Fav.objects.filter(user = request.user)
        list = []
        for item in query:
            list.append(item.symbol)
        return Response(list,status= status.HTTP_200_OK)

def checkpin(request):
    if not len(Pin.objects.filter(user = request.user)):
        return False
    elif not len(PinVer.objects.filter(user = request.user)):
        return False
    else:
        p = PinVer.objects.get(user = request.user)
        if p.date + timedelta(minutes=30) < timezone.now():
            for item in PinVer.objects.filter(user = request.user):
                item.delete()
            return False
        else:
            return True


class pined(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not len(Pin.objects.filter(user = request.user)):
            p = Pin(pin = request.data['pin'], user = request.user)
            p.save()
            p = PinVer(user = request.user)
            p.save()
            return Response(status= status.HTTP_200_OK)
        if Pin.objects.get(user = request.user).pin == request.data['pin']:
            for item in PinVer.objects.all():
                item.delete()
                p = PinVer(user = request.user)
                p.save()
                return Response(status= status.HTTP_200_OK)
        else:
            return Response(status= status.HTTP_403_FORBIDDEN)



class token(APIView):
    def get(self, request):
        r = requests.post('https://api.kucoin.com/api/v1/bullet-public')
        r = r.json()['data']
        return Response(r['token'])

class buy(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not checkpin(request):
            return Response(False)
        request.data['status'] = True
        r = requests.get(f'https://api-futures.kucoin.com/api/v1/level2/snapshot?symbol={request.data["currency"]}')
        r = r.json()['data']['asks']
        if request.data['market']:
            request.data['status'] = True
        else:
            request.data['status'] = False
        if float(request.data['price']) > float(r[0][0]):
            request.data['status'] = True
        else:
            request.data['status'] = False
        request.data['user'] = request.user.id
        serializer = OrderSerializer(data = request.data)
        wallet = Wallet.objects.get(user = request.user)
        sum = float(request.data['amount']) * float(request.data['start'])
        if serializer.is_valid():
            if wallet.balance < sum :
                return Response(status=status.HTTP_400_BAD_REQUEST) 
            wallet.balance = wallet.balance - sum
            wallet.save()
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class sell(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not checkpin(request):
            return Response(False)
        request.data['status'] = True
        r = requests.get(f'https://api-futures.kucoin.com/api/v1/level2/snapshot?symbol={request.data["currency"]}')
        r = r.json()['data']['bids']
        if request.data['market']:
            request.data['status'] = True
        else:
            request.data['status'] = False
        if float(request.data['price']) < float(r[0][0]):
            request.data['status'] = True
        else:
            request.data['status'] = False
        request.data['user'] = request.user.id
        serializer = OrderSerializer(data = request.data)
        wallet = Wallet.objects.get(user = request.user)
        sum = float(request.data['amount']) * float(request.data['start'])
        if serializer.is_valid():
            if wallet.balance < sum :
                return Response(status=status.HTTP_400_BAD_REQUEST) 
            wallet.balance = wallet.balance - sum
            wallet.save()
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class historicalbuy(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.data['status'] = True
        request.data['user'] = request.user.id
        request.data['date'] = request.data['date1']
        request.data['start'] = float(request.data['price1'])
        request.data['price'] = float(request.data['price1'])
        serializer = OrderSerializer(data = request.data)
        wallet = Wallet.objects.get(user = request.user)
        sum = float(request.data['amount']) * float(request.data['start'])
        if serializer.is_valid():
            if wallet.balance < sum :
                return Response(status=status.HTTP_400_BAD_REQUEST) 
            wallet.balance = wallet.balance - sum
            wallet.save()
            serializer.save()
            if 'price2' in request.data:
                order = Order.objects.get(start = float(request.data['price1']), date = request.data['date1'])
                amount = float(request.data['amount'])
                price = float(request.data['price2'])
                fee = float(request.data['fee'])
                order.amount = order.amount - float(request.data['amount'])
                order.save()
                cc = ClosedOrder(currency = order.currency,type = order.type, user = order.user, amount = float(request.data['amount']), price = float(request.data['price2']), startprice = order.price, leverage = order.leverage, funding = order.funding, pnl = (float(request.data['amount']) * float(request.data['price2']))- float(request.data['fee']) - (order.amount * order.start), fee = float(request.data['fee']))
                cc.save()
                wallet = Wallet.objects.get(user = request.user)
                wallet.balance = wallet.balance + ((amount * price) - fee)
                wallet.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class historicalsell(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.data['status'] = True
        request.data['user'] = request.user.id
        request.data['date'] = request.data['date1']
        request.data['start'] = float(request.data['price1'])
        request.data['price'] = float(request.data['price1'])
        serializer = OrderSerializer(data = request.data)
        wallet = Wallet.objects.get(user = request.user)
        sum = float(request.data['amount']) * float(request.data['start'])
        if serializer.is_valid():
            if wallet.balance < sum :
                return Response(status=status.HTTP_400_BAD_REQUEST) 
            wallet.balance = wallet.balance - sum
            wallet.save()
            serializer.save()
            if 'price2' in request.data:
                order = Order.objects.get(start = float(request.data['price1']), date = request.data['date1'])
                amount = float(request.data['amount'])
                price = float(request.data['price2'])
                fee = float(request.data['fee'])
                order.amount = order.amount - float(request.data['amount'])
                order.save()
                cc = ClosedOrder(currency = order.currency,type = order.type, user = order.user, amount = float(request.data['amount']), price = float(request.data['price2']), startprice = order.price, leverage = order.leverage, funding = order.funding, pnl = (float(request.data['amount']) * float(request.data['price2']))- float(request.data['fee']) - (order.amount * order.start), fee = float(request.data['fee']))
                cc.save()
                wallet = Wallet.objects.get(user = request.user)
                wallet.balance = wallet.balance + ((amount * price) - fee)
                wallet.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class m_close(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not checkpin(request):
            return Response(False)
        order = Order.objects.get(id= request.data['id'])
        amount = float(request.data['amount'])
        price = float(request.data['price'])
        fee = float(request.data['fee'])
        order.amount = order.amount - float(request.data['amount'])
        order.save()
        cc = ClosedOrder(currency = order.currency,type = order.type, user = order.user, amount = float(request.data['amount']), price = float(request.data['price']), startprice = order.price, leverage = order.leverage, funding = order.funding, pnl = (float(request.data['amount']) * float(request.data['price']))- float(request.data['fee']) - (order.amount * order.start), fee = float(request.data['fee']))
        cc.save()
        wallet = Wallet.objects.get(user = request.user)
        wallet.balance = wallet.balance + ((amount * price) - fee)
        wallet.save()
        print(wallet.balance , amount, price, fee)
        return Response(status= status.HTTP_200_OK)

class l_close(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not checkpin(request):
            return Response(False)
        order = Order.objects.get(id= int(request.data['id']))
        amount = request.data['amount']
        price = request.data['price']
        order.limit = float(price)
        order.limit_amount = float(amount)
        order.save()
        return Response(status= status.HTTP_200_OK)

class l_cancel(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not checkpin(request):
            return Response(False)
        order = Order.objects.get(id= int(request.data['id']))
        order.canceled = True
        order.status = True
        order.save()
        return Response(status= status.HTTP_200_OK)

class tp_cancel(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not checkpin(request):
            return Response(False)
        order = Order.objects.get(id= int(request.data['id']))
        order.tp = None
        order.save()
        return Response(status= status.HTTP_200_OK)

class sl_cancel(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not checkpin(request):
            return Response(False)
        order = Order.objects.get(id= int(request.data['id']))
        order.sl = None
        order.save()
        return Response(status= status.HTTP_200_OK)


class tpsl_send(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not checkpin(request):
            return Response(False)
        order = Order.objects.get(id= request.data['id'])
        tp = request.data['tp']
        tp_amount = request.data['tp_amount']
        sl = request.data['sl']
        sl_amount = request.data['sl_amount']
        order.tp = tp
        order.tp_amount = tp_amount
        order.sl = sl
        order.sl_amount = sl_amount
        order.save()
        return Response(status= status.HTTP_200_OK)


class positions(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = Order.objects.filter(status = True, canceled = False ,user = request.user.id, amount__gt = 0 , limit = None)
        serializer = OrderSerializer(query ,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class orders(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = Order.objects.filter(status = False, user = request.user.id)
        serializer = OrderSerializer(query ,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class allorders(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = Order.objects.filter(user = request.user.id , status = True)
        serializer = OrderSerializer(query ,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class closeorders(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = ClosedOrder.objects.filter(user = request.user.id)
        serializer = CloseOrderSerializer(query ,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class balance(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not len(Wallet.objects.filter(user = request.user)):
            wa = Wallet.objects.filter(user = request.user, currency = Currency.objects.get(brand = 'USDT'))
            wa.save()
        query = Wallet.objects.filter(user = request.user)
        serializer = WalletSerializer(query, many = True)
        return Response(serializer.data)


class get_price(APIView):

    def post(self, request):
        currency = request.data['currency']
        date = request.data['date']
        r = requests.get(f'https://api-futures.kucoin.com/api/v1/kline/query?symbol={currency}&granularity=1&from={date}')
        print(r.json()['data'][0][1])
        return Response(r.json()['data'][0][1])

class symbols(APIView):

    def get(self, request):
        r = requests.get('https://api-futures.kucoin.com/api/v1/contracts/active')
        r = r.json()
        return Response(r)

    def post(self, request):
        r = requests.get(f'https://api-futures.kucoin.com/api/v1/contracts/{request.data["sym"]}')
        r = r.json()
        return Response(r)







# Admin


class users(APIView):
    def post(self, request):
        user = User(username = request.data['username'], password = make_password(request.data['password']))
        user.save()
        query = User.objects.filter(is_superuser = False)
        serializer = UserSerializer(query, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        query = User.objects.filter(is_superuser = False)
        serializer = UserSerializer(query, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        query = User.objects.get(id = int(request.data['id']))
        query.set_password(request.data['password'])
        query.save()
        query = User.objects.filter(is_superuser = False)
        serializer = UserSerializer(query, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class balances(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = Wallet.objects.all()
        serializer = WalletSerializer(query, many = True)
        return Response(serializer.data)

    def put(self, request):
        query = Wallet.objects.get(id = int(request.data['id']))
        query.balance = float(request.data['balance'])
        query.save()
        query = Wallet.objects.all()
        serializer = WalletSerializer(query, many = True)
        return Response(serializer.data)