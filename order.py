from enum import Enum
import heapq

class Direction(Enum):
    buy = 0
    sell = 1

class Order(object):
    def __init__(self, order_id, quantity, broker, timestamp, direction):
        self.order_id = order_id
        self.quantity = quantity
        self.broker = broker
        self.timestamp = timestamp
        self.direction = direction

    def get_order_id(self):
        return self.order_id

    def get_broker(self):
        return self.broker

    def get_timestamp(self):
        return self.timestamp

    def get_direction(self):
        return self.direction

    def get_quantity(self):
        return self.quantity


class LimitOrder(Order):
    def __init__(self, order_id, quantity, broker, timestamp, direction, price):
        Order.__init__(self, order_id, quantity, broker, timestamp, direction)
        self.price = price

    def signed_price(self):
        if self.direction == Direction.buy.value:
            return +self.price
        else:
            return -self.price

    def __lt__(self, other):
        return (self.signed_price() > other.signed_price()) \
            or (self.signed_price() == other.signed_price()
                   and self.timestamp < other.timestamp)

    def __eq__(self, other):
        return (self.price == other.price) \
            and (self.timestamp == other.timestamp)

    def __gt__(self, other):
        return not (self.__lt__(other) or self.__eq__(other))

    def __str__(self):
        return "(" \
               "order_id: %s, quantity: %d, " \
               "broker: %s, timestamp: %d, " \
               "direction: %d, price: %8.2f" \
               ")" % \
               (self.order_id, self.quantity, self.broker, self.timestamp, self.direction, self.price)


    def set_quantity(self, value):
        self.quantity = value


class OrderBook(object):
    def __init__(self):
        self.bids = [] # empty list
        self.asks = [] # empty list
        # you use these lists to create priority queues.
        # you need priority queues to access to the top element in O(1)
        self.order_index = dict()
        # you need a dictionary or a unordered Hash map to access any element in O(1)
        # Based on a key which is the order_id
        # insertion time complexity

    def add(self, lo):
        if lo.direction == Direction.buy.value:
            print("A new bid is added. "
                  "(" \
               "order_id: %s, quantity: %d, " \
               "broker: %s, price: %8.2f" \
               ")" % \
                (lo.order_id, lo.quantity, lo.broker, lo.price)
)
            heapq.heappush(self.bids, lo)
            self.order_index[ lo.order_id ] = lo
        else:
            heapq.heappush(self.asks, lo)
            print("A new ask is added. "
                  "(" \
               "order_id: %s, quantity: %d, " \
               "broker: %s, price: %8.2f" \
               ")" % \
                (lo.order_id, lo.quantity, lo.broker, lo.price))
            self.order_index[ lo.order_id ] = lo
        if self.asks and self.bids:
            self.__match()

    def __match(self):
        best_bid = self.bids[0]
        best_ask = self.asks[0]
        if best_bid.price >= best_ask.price:
            if best_bid.quantity > best_ask.quantity:
                remain = best_bid.quantity - best_ask.quantity
                print('A bid (ID: %s) and an ask (ID: %s) are matched. '
                      'The ask (ID: %s) is filled with the quantity %d.' \
                      % (best_bid.order_id, best_ask.order_id, best_ask.order_id, best_ask.quantity))
                self.bids[0].set_quantity(remain)
                heapq.heappop(self.asks)
                self.__match()

            elif best_bid.quantity < best_ask.quantity:
                remain = best_ask.quantity - best_bid.quantity
                print('A bid (ID: %s) and an ask (ID: %s) are matched. '
                      'The bid (ID: %s) is filled with the quantity %d.' \
                      % (best_bid.order_id, best_ask.order_id, best_bid.order_id, best_bid.quantity))
                self.asks[0].set_quantity(remain)
                heapq.heappop(self.bids)
                self.__match()

            else:
                print('A bid (ID: %s) and an ask (ID: %s) are matched. '
                      'Both are filled with the quantity %d.' \
                      % (best_bid.order_id, best_ask.order_id, best_ask.quantity))
                heapq.heappop(self.bids)
                heapq.heappop(self.asks)
