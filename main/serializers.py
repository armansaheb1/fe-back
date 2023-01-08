from .models import Order, Wallet, ClosedOrder
from rest_framework import serializers
from django.contrib.auth.models import User

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            "id",
            "user",
            "currency",
            "type",
            "amount",
            "leverage",
            "price",
            "start",
            "date",
            "date",
            "status",
            "tp",
            "sl",
            "limit",
            "closed",
            "canceled",
            "funding",
            "limit_amount"
        )

class CloseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClosedOrder
        fields = (
            "id",
            "user",
            "currency",
            "type",
            "amount",
            "leverage",
            "price",
            "date",
            "funding",
            "pnl",
            "fee",
        )


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = (
            "id",
            "currency",
            "balance",
            "get_user"
        )



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
        )