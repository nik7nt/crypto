import json
from binance.client import Client


class BinanceFuturesAPI:
    def __init__(self, binance_api_key=None, binance_api_secret_key=None):
        self.api_key = binance_api_key
        self.api_secret_key = binance_api_secret_key
        self.client = self._create_client()

    def _create_client(self):
        return Client(self.api_key, self.api_secret_key)

    def new_market_buy_order(self, symbol, quantity):
        return self.new_order(symbol, "BUY", "MARKET", quantity)

    def new_market_stop_loss_order(self, symbol, quantity, stop_price):
        return self.new_order(symbol, "SELL", "STOP_MARKET", quantity, stop_price)

    def new_market_take_profit_order(self, symbol, quantity, stop_price):
        return self.new_order(symbol, "SELL", "TAKE_PROFIT_MARKET", quantity, stop_price)

    def new_order(self, symbol, side, type_order, quantity, stop_price=None):
        """
        Send a new order
        """
        data = {
            'symbol': symbol,
            'side': side,
            'type': type_order,
            'quantity': quantity,
        }

        if stop_price:
            data['stopPrice'] = stop_price

        return self._request(data)

    def change_leverage(self, symbol, value):
        return self.client.futures_change_leverage(symbol=symbol, leverage=value)

    def _request(self, data):
        r = self.client.futures_create_order(**data)

        return json.dumps(r)

    def ping(self):
        return self.client.ping()

    def get_server_time(self):
        return self.client.get_server_time()

    def _get_account_balance(self):
        return self.client.futures_account_balance()

    def get_symbol_market_price(self, symbol):
        return float(self.client.get_symbol_ticker(symbol=symbol)["price"])

    def get_usdt_withdraw_available(self):
        account_balance_data = self._get_account_balance()
        for item in account_balance_data:
            if item["asset"] == "USDT":
                return float(item["withdrawAvailable"])

    def get_usdt_full_balance(self):
        account_balance_data = self._get_account_balance()
        for item in account_balance_data:
            if item["asset"] == "USDT":
                return float(item["balance"])

    def get_price_precision(self, symbol):
        info = self.client.futures_exchange_info()
        precision_data = {}
        for x in info['symbols']:
            if x['symbol'] == symbol:
                precision_data.update({
                    "quantityPrecision": x["quantityPrecision"],
                    "pricePrecision": x["pricePrecision"],
                })

        return precision_data
