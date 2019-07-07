import bipy as bp
import json
import datetime
import time


def ping_time(client):
    timestamp = client.ping_time()
    td = datetime.datetime.fromtimestamp(int(timestamp['serverTime']) / 1000)
    print('Connected... server time is:', td)


def get_min_order_id(orders):
    if len(orders) == 0:
        return 0
    ids = []
    for o in orders:
        ids.append(int(o['orderId']))
    return min(ids)


def order_difference_new(order_watch_list, orders):
    added = 0
    new_orders = filter(lambda o: o['status'] == bp.BiPy.ORDER_STATUS_NEW, orders)
    for o in new_orders:
        id = o['orderId']
        if len(order_watch_list) > 0:
            f = list(filter(lambda i: i['orderId'] == id, order_watch_list))
            if len(f) == 0:
                print(f'New order {id} detected, adding...')
                order_watch_list.append(o)
                added += 1
    else:
        print(f'Adding first order: {id}...')
        order_watch_list.append(o)
        added += 1
    if added > 0:
        print(f'{added} new orders added to watch list...')
    else:
        print('No new orders detected.')


# def order_difference_filled(order_watch_list, orders):
# filled_orders =

def get_orders(client, order_watch_list, **kwargs):
    """
        filter e.g. status='NEW'
        ORDER:
        symbol : TRXBTC
        orderId : 95518149
        clientOrderId : ios_f4576fe09e094614af7a6c88773af717
        price : 0.00000625
        origQty : 3272.00000000
        executedQty : 3272.00000000
        cummulativeQuoteQty : 0.02045000
        status : FILLED
        timeInForce : GTC
        type : LIMIT
        side : BUY
        stopPrice : 0.00000000
        icebergQty : 0.00000000
        time : 1551303552705
        updateTime : 1551319830936
        isWorking : True

    """
    orders = client.get_all_orders(**kwargs)
    print(f'Orders received in query: {len(orders)}')
    # check for new orders
    # order_difference_new(order_watch_list, orders)


def order_print(orders):
    print(f'The current, tracked order list is:	')
    for o in orders:
        print('ORDER:')
        for i in o:
            print(f'	{i} : {o[i]}')


def process_key_press(key_press):
    if key_press.ToUpper() == 'L':
        order_print()


def main():
    # constants and config
    poll_interval_seconds = 5
    trading_pair = 'TRXBTC'
    # load config
    with open('_config.json', 'r') as f:
        config = json.load(f)

    # logon to binance
    secret = config['DEFAULT']['SECRET_KEY']
    key = config['DEFAULT']['API_KEY']
    # create client
    client = bp.BiPy(key, secret)
    order_watch_list = []
    # ping test
    ping_time(client)
    # load orders into watch-list
    get_orders(client, order_watch_list, symbol=trading_pair)
    first_order = get_min_order_id(order_watch_list)
    print(f'First open order id is: {first_order}. All orders will be fetched in respect of this until restart.')

    # trade
    while True:
        ping_time(client)
        # check orders
        get_orders(client, order_watch_list, symbol=trading_pair, orderId=str(first_order))
        # update watch list

        # evaluate watchlist
        price = client.get_price(symbol=trading_pair)['price']
        print(f'Current {trading_pair} price: {price}')
        # print(f'current {TRADING_PAIR} price: {price[1]}')
        # order_print(current_orders)
        # place orders
        time.sleep(poll_interval_seconds)


if __name__ == '__main__':
    main()
