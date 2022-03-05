from rest_framework import serializers

from webhooks.models import CandleContent, TradeRequest


class CandleContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = CandleContent
        fields = "__all__"


class TradeRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = TradeRequest
        fields = "__all__"