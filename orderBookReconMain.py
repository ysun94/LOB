from order import LimitOrder, OrderBook

orders = [LimitOrder('1019', 62, 'L', 1, 1, 10702),
LimitOrder('1006', 8, 'R',1, 1, 10665),
LimitOrder('1004', 74, 'C', 2, 0, 9092),
LimitOrder('1012', 92, 'H', 2, 1, 9684),
LimitOrder('1005', 83, 'X', 4, 1, 9841),
LimitOrder('1017', 89, 'D', 5, 1, 9784),
LimitOrder('1001', 40, 'R', 5, 0, 9521),
LimitOrder('1007', 19, 'N', 5, 1, 10388),
LimitOrder('1013', 97, 'J', 6, 0, 9147),
LimitOrder('1010', 41, 'R', 7, 0, 10572),
LimitOrder('1015', 94, 'G', 8, 0, 10077),
LimitOrder('1003', 91, 'Q', 8, 1, 8695),
LimitOrder('1009', 59, 'S', 10, 0, 11066),
LimitOrder('1018', 68, 'F', 12, 0, 8225),
LimitOrder('1008', 3, 'K', 12, 1, 9849),
LimitOrder('1016', 4, 'D', 13, 0, 8726),
LimitOrder('1002', 83, 'O', 16, 0, 10876),
LimitOrder('1011', 38, 'D', 18, 0, 11142),
LimitOrder('1014', 54, 'Q', 19, 1, 9442),
LimitOrder('1000', 68, 'S', 20, 1, 9287)]


book = OrderBook()

index = 0
for order in orders:
    print('---------------------------')
    print('Event [' + str(index) + ']: ')
    book.add( order )
    print('---------------------------')
    index += 1

    print('Bid (Buy-side) priority queue:')
    if ( book.bids ):
        for i in book.bids:
            print(i)
    else:
        print('Bid is empty.')

    print('Ask (Sell-side) priority queue:')
    if ( book.asks ):
        for i in book.asks:
            print(i)
    else:
        print('Ask is empty.')

    print('\n')

    
