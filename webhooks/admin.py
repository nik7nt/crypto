from django.contrib import admin

# Register your models here.
from .models import CandleContent, TradeRequest

admin.site.register(CandleContent)
admin.site.register(TradeRequest)