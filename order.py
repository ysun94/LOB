from enum import Enum
import heapq
import copy

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

    def get_price(self):
        return self.price

class PriorityQueue(object):
    def __init__(self):
        self.heap = []

    def push(self, lo):
        heapq.heappush(self.heap, lo)

    def pop(self):
        heapq.heappop(self.heap)

    def empty(self):
        if (not self.heap):
            return True
        else:
            return False

    def top(self):
        if(not self.empty()):
            return self.heap[0]

class OrderBook(object):
    def __init__(self):
        self.bids = PriorityQueue()
        self.asks = PriorityQueue()
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
            self.bids.push(lo)
            # heapq.heappush(self.bids, lo)
            self.order_index[ lo.order_id ] = lo
        else:
            self.asks.push(lo)
            # heapq.heappush(self.asks, lo)
            print("A new ask is added. "
                  "(" \
               "order_id: %s, quantity: %d, " \
               "broker: %s, price: %8.2f" \
               ")" % \
                (lo.order_id, lo.quantity, lo.broker, lo.price))
            self.order_index[ lo.order_id ] = lo
        self.__match()

    def __match(self):
        if (not self.asks.empty()) and (not self.bids.empty()):
            best_bid = self.bids.top()
            best_ask = self.asks.top()
            if best_bid.price >= best_ask.price:
                if best_bid.quantity > best_ask.quantity:
                    remains = best_bid.quantity - best_ask.quantity
                    print('A bid (ID: %s) and an ask (ID: %s) are matched. '
                          'The ask (ID: %s) is filled with the quantity %d.' \
                          % (best_bid.order_id, best_ask.order_id, best_ask.order_id, best_ask.quantity))
                    self.bids.top().set_quantity(remains)
                    self.order_index[best_ask.order_id] = 'Deleted'
                    self.asks.pop()
                    # heapq.heappop(self.asks)
                    self.__match()

                elif best_bid.quantity < best_ask.quantity:
                    remains = best_ask.quantity - best_bid.quantity
                    print('A bid (ID: %s) and an ask (ID: %s) are matched. '
                          'The bid (ID: %s) is filled with the quantity %d.' \
                          % (best_bid.order_id, best_ask.order_id, best_bid.order_id, best_bid.quantity))
                    self.asks.top().set_quantity(remains)
                    self.order_index[best_bid.order_id] = 'Deleted'
                    self.bids.pop()
                    # heapq.heappop(self.bids)
                    self.__match()

                else:
                    print('A bid (ID: %s) and an ask (ID: %s) are matched. '
                          'Both are filled with the quantity %d.' \
                          % (best_bid.order_id, best_ask.order_id, best_ask.quantity))
                    self.order_index[best_ask.order_id] = 'Deleted'
                    self.order_index[best_bid.order_id] = 'Deleted'
                    self.asks.pop()
                    self.bids.pop()
                    # heapq.heappop(self.bids)
                    # heapq.heappop(self.asks)

    def spread(self):
        if (not self.bids.empty() and not self.asks.empty()):
            # Spread is always non-negative
            assert self.asks.top().get_price() - self.bids.top().get_price() >= 0
            return self.asks.top().get_price() - self.bids.top().get_price()

    def mid_price(self):
        if( not self.bids.empty() and not self.asks.empty() ):
            return (self.asks.top().get_price() + self.bids.top().get_price())/2.0

    def micro_price(self):
        # Volume Weighted Average Price
        if( not self.bids.empty() and not self.asks.empty() ):
            best_ask_price  = self.asks.top().get_price()
            best_ask_volume = self.asks.top().get_quantity()
            best_bid_price  = self.bids.top().get_price()
            best_bid_volume = self.bids.top().get_quantity()
            return ( best_bid_volume/(best_ask_volume + best_bid_volume) )*best_ask_price \
                   + ( best_ask_volume/(best_ask_volume + best_bid_volume) )*best_bid_price

    def info(self, order_id):
        if order_id in self.order_index:
            return self.order_index[order_id]
        # Otherwise return None.

    def show_state(self):
        print("\n")
        print("Buy-side (Bid) priority queue:")
        temp = copy.deepcopy(self.bids)
        # Otherwise, it will reference to the same object
        # and 'temp.pop()' will also pop the element in 'self.bids'
        while (not temp.empty()):
            print(temp.top())
            temp.pop()
        print("\n")

        print("Sell-side (Ask) priority queue:")
        temp = copy.deepcopy(self.asks)
        while (not temp.empty()):
            print(temp.top())
            temp.pop()
        print("\n")

        print("Order Book statistics:")
        print( "Spread:      " + str(self.spread())      + " £")
        print( "Mid price:   " + str(self.mid_price())   + " £")
        print( "Micro price: " + str(self.micro_price()) + " £")
        print("\n")

        print("Current Status: ")
        for i in self.order_index:
            print("ID:", i,"-", self.order_index[i])
        print('\n')

