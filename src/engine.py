import class_list as c
import robin_stocks.robinhood as r
import BuySell as bs
import globaldict as gd


def last_trade (crypto_asset, flag=None):
    """Flag defaults to none which the bots sets the flag based off old trade.  Flag of 1 means you want to buy Bitcoin.  Flag of -1 means you want to sell Bitcoin"""
    assert type(crypto_asset) == str
    if flag == 1:
        print("Looking for BUYS")
        return 1
    if flag == -1:
        print("Looking for SELLS")
        return -1
    if flag == None:
        trade_list = r.orders.get_all_crypto_orders()
        last_trade = None
        for i in range(len(trade_list)):
            if trade_list[i]['currency_pair_id'] == crypto_asset:
                last_trade = trade_list[i]
                print('Trade Found')
                break
            else:
                print('Searching for Last Trade')
        if last_trade == None:
            print('No trade was found in histroy.  Please set flag parameter')
    if last_trade['side'] == 'sell' and last_trade['state'] == 'filled':
        return 1
    if last_trade['side'] == 'buy' and last_trade['state'] == 'filled':
        return -1 
    else:
        print('There maybe a pending uncleared trade in your account. Last trade of this security has note settled')
        return AssertionError

def engine(flag, key, trade_exposure, asset):
    flag = flag
    key = key

    assert flag == 1 or flag == -1
    while True:
        #take_profit
        #amount adjuster
        if flag == 1:
            flag = gd.Global_Dictionary[key](flag)
            cancel_event = bs.limit_crypto_buy(asset, trade_exposure, ladder=True)
            if cancel_event == 0:
                flag = -1
            if cancel_event == 1:
                flag = 1
        if flag == -1:
            flag = gd.Global_Dictionary[key](flag)
            cancel_event = bs.limit_crypto_sell(asset, trade_exposure, ladder=True)
            if cancel_event == 0:
                flag = 1
            if cancel_event == -1:
                flag = -1


