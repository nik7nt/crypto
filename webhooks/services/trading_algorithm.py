import telebot
import datetime
from crypto.settings import TOKEN_TELEGRAM_BOT, BINANCE_API_KEY, BINANCE_API_SECRET_KEY
from webhooks.models import CandleContent, TradeRequest
from webhooks.serializer import TradeRequestSerializer
from webhooks.services.binance_bot import BinanceFuturesAPI

bot = telebot.TeleBot(TOKEN_TELEGRAM_BOT)
bot.config['api_key'] = TOKEN_TELEGRAM_BOT


class TradeAlgorithm:
    def __init__(self, **kwargs):
        self.crypto_pair = kwargs.get("crypto_pair")
        self.close_price = kwargs.get("close_price")

    def _send_to_bot(self):
        chat_id = -1001388854956
        bb = self._binance_bot().get_usdt_full_balance()
        ab = self._binance_bot().get_usdt_withdraw_available()
        market_price = self._binance_bot().get_symbol_market_price(self.crypto_pair.replace("PERP", ""))
        text = f"""Баланс: {bb};\nБаланс свободных для покупки средств: {ab};\nКриптопара: {self.crypto_pair};\nВремя отправления хука на Binance: {datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.%S")};\nПриблизительная цена по маркету в момент отправки хука запроса на покупку: {market_price}"""

        bot.send_message(chat_id=chat_id,
                         text=text)

        return 200

    def execution_condition(self):
        all_content_candles = CandleContent.objects.filter(
            crypto_pair=self.crypto_pair).order_by('-created_at')[:2]
        if len(all_content_candles) >= 2:
            delta = datetime.timedelta(minutes=16)
            delta_trade = datetime.timedelta(hours=2)
            trade_period_pass = datetime.datetime.utcnow() - delta_trade
            previous_trade_request = TradeRequest.objects.filter(
                crypto_pair=self.crypto_pair).filter(
                created_at__gt=trade_period_pass
            )
            if ((all_content_candles[0].created_at - all_content_candles[1].created_at) < delta) and (
                    len(previous_trade_request) == 0):
                if (all_content_candles[0].close_price > all_content_candles[1].close_price) and (
                        all_content_candles[0].low_price >= all_content_candles[1].low_price):
                    self._add_to_db(self.crypto_pair)
                    # self._binance_trade(self.crypto_pair.replace("PERP", ""))
                    self._send_to_bot()
            return 400
        return 404

    def _add_to_db(self, cr_pr):
        trade_request = TradeRequestSerializer(data={"crypto_pair": cr_pr})
        if trade_request.is_valid():
            trade_request.save()

        return 200

    def _binance_bot(self):
        return BinanceFuturesAPI(BINANCE_API_KEY, BINANCE_API_SECRET_KEY)

    def _binance_trade(self, symbol):
        binance_bot = self._binance_bot()
        leverage = binance_bot.change_leverage(symbol=symbol, value=10).get("leverage", "")
        usdt_full_balance = binance_bot.get_usdt_full_balance()
        data_precision = binance_bot.get_price_precision(symbol)
        symbol_market_price = binance_bot.get_symbol_market_price(symbol=symbol)

        if data_precision["quantityPrecision"] == 0:
            quantity = round(usdt_full_balance * 0.1 / symbol_market_price * leverage)
        else:
            quantity = round(usdt_full_balance * 0.1 / symbol_market_price * leverage, data_precision["quantityPrecision"])

        binance_bot.new_market_buy_order(symbol=symbol, quantity=quantity)

        binance_bot.new_market_stop_loss_order(
            symbol=symbol,
            quantity=quantity,
            stop_price=round(symbol_market_price * 0.994, data_precision["pricePrecision"]))

        binance_bot.new_market_take_profit_order(
            symbol=symbol,
            quantity=quantity,
            stop_price=round(symbol_market_price * 1.004, data_precision["pricePrecision"]))

        return 200
