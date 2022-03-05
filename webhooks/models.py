from django.contrib.auth.models import AbstractUser
from django.db import models


class CandleContent(models.Model):
    SIGNAL_TYPES = [
        ("L", "LONG"),
        ("S", "SHORT"),
    ]
    type_signal = models.CharField("тип сигнала", max_length=1, choices=SIGNAL_TYPES, default="L")
    crypto_pair = models.CharField("криптовалютная пара", max_length=20, null=True, blank=True)
    open_price = models.FloatField("цена на открытии свечи")
    close_price = models.FloatField("цена на закрытии свечи")
    low_price = models.FloatField("минимальная цена за свечу")
    high_price = models.FloatField("максимальная цена за свечу")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crypto_pair} {self.created_at}"


class TradeRequest(models.Model):

    ORDER_TYPES = [
        ("L", "LONG"),
        ("S", "SHORT"),
    ]
    type_order = models.CharField("тип ордера", max_length=1, choices=ORDER_TYPES, default="L")
    crypto_pair = models.CharField("криптовалютная пара", max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crypto_pair} {self.created_at}"


class User(AbstractUser):
    # username = None
    first_name = None
    last_name = None
    full_name = models.CharField("полное имя", max_length=150, blank=True)
    email = models.EmailField("email адрес", unique=True)

    def __str__(self):
        return self.full_name if self.full_name else self.email


class APIProfile(models.Model):
    market = models.CharField(verbose_name="биржа", default="Binance Futures", max_length=100)
    api_key = models.CharField(verbose_name="ключ api", max_length=200)
    api_secret_key = models.CharField(verbose_name="секретный ключ api", max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="пользователь")

    def __str__(self):
        return f"{self.market}"
