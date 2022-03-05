import telebot
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from webhooks.serializer import CandleContentSerializer
from webhooks.services.trading_algorithm import TradeAlgorithm


class TradingView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        content_candle = CandleContentSerializer(data=request.data)
        if content_candle.is_valid():
            content_candle.save()

        trade_alg = TradeAlgorithm(**request.data)
        status = trade_alg.execution_condition()

        if status == 200:
            return Response(status=200)
        else:
            return Response(status=400)

