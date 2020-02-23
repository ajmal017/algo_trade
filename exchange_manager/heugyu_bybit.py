import json
from bybit import bybit

###################################### KEY #################
BYBIT_API_KEY = 'g23TGVkHvDcj9db8dp'
BYBIT_PRIVATE_KEY = 'WC1hep7AOXqCLNKnRv5nf4KZZrdODzbVZN5I'
############################################################


class Bybit(object):
    def __init__(self, test=True, api_key=BYBIT_API_KEY, api_secret=BYBIT_PRIVATE_KEY, symbol='BTCUSD'):
        self.test = test
        self.api_key = api_key
        self.api_secret = api_secret
        self.symbol = symbol
        self.client = bybit(
            test=self.test,
            api_key=self.api_key,
            api_secret=self.api_secret
        )

    def is_position(self):
        current_position = self.client.Positions.Positions_myPosition().result()[0]['result'][0]
        return current_position

    def get_active_orders(self):
        order_history = self.client.Order.Order_getOrders().result()[0]['result']['data']
        active_orders = [order for order in order_history if order['order_status'] == 'New']
        return active_orders

    def cancel_active_orders(self, orders):
        if len(orders) > 0:
            for _, order in enumerate(orders):
                order_id = order['order_id']
                order_symbol = order['symbol']
                order_side = order['side']
                order_price = order['price']
                order_qty = order['qty']
                self.client.Order.Order_cancel(order_id=order_id).result()
            return True
        else:
            return False

    def set_active_order(self, side, order_type, qty, price):
        pass
