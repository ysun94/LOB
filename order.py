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
        if self.direction is Direction.buy:
            return +self.price
        else:
            return -self.price

    def __gt__(self, other):
        return (self.signed_price() > other.signed_price()) \
            or (self.signed_price() == other.signed_price()
                   and self.timestamp < other.timestamp)

    def __eq__(self, other):
        return (self.price == other.price) \
            and (self.timestamp == other.timestamp)

    def __lt__(self, other):
        return not (self.__gt__(other) or self.__eq__(other))

    def __str__(self):
        return "The order %s information is shown as follows:\n" \
               "----------------\n" \
               "order_id: %s\nquantity: %d\n" \
               "broker: %s\ntimestamp: %d\n" \
               "direction: %d\nprice: %8.2f\n" \
               "----------------" % \
               (self.order_id, self.order_id, self.quantity, self.broker, self.timestamp, self.direction, self.price)


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
        if lo.direction is Direction.buy:
            heapq.heappush(self.bids, lo)
            self.order_index[ lo.order_id ] = lo
        else:
            heapq.heappush(self.asks, lo)
            self.order_index[ lo.order_id ] = lo


'''
order1019 = LimitOrder('1019', 62, 'L', 1, 1, 10702)
order1006 = LimitOrder('1006', 8, 'R',1, 1, 10665)
order1004 = LimitOrder('1004', 74, 'C', 2, 0, 9092)
order1012 = LimitOrder('1012', 92, 'H', 2, 1, 9684)
order1005 = LimitOrder('1005', 83, 'X', 4, 1, 9841)
order1017 = LimitOrder('1017', 89, 'D', 5, 1, 9784)
order1001 = LimitOrder('1001', 40, 'R', 5, 0, 9521)
order1007 = LimitOrder('1007', 19, 'N', 5, 1, 10388)
order1013 = LimitOrder('1013', 97, 'J', 6, 0, 9147)
order1010 = LimitOrder('1010', 41, 'R', 7, 0, 10572)
order1015 = LimitOrder('1015', 94, 'G', 8, 0, 10077)
order1003 = LimitOrder('1003', 91, 'Q', 8, 1, 8695)
order1009 = LimitOrder('1009', 59, 'S', 10, 0, 11066)
order1018 = LimitOrder('1018', 68, 'F', 12, 0, 8225)
order1008 = LimitOrder('1008', 3, 'K', 12, 1, 9849)
order1016 = LimitOrder('1016', 4, 'D', 13, 0, 8726)
order1002 = LimitOrder('1002', 83, 'O', 16, 0, 10876)
order1011 = LimitOrder('1011', 38, 'D', 18, 0, 11142)
order1014 = LimitOrder('1014', 54, 'Q', 19, 1, 9442)
order1000 = LimitOrder('1000', 68, 'S', 20, 1, 9287)
order1015 = LimitOrder('1015', 94, 'G', 8, 0, 10077)
print(bids[-1]) do not use this
'''
