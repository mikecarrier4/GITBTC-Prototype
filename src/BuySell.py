import engine as e
import Utility as u
import robin_stocks.robinhood as r
import class_list as c
import Returns as re

"""Basic Market Orders"""

def buy_crypto (trading_asset, trade_exposure):
    order = r.orders.order_buy_crypto_by_price(
    symbol = trading_asset,
    amountInDollars = float(trade_exposure),
    timeInForce='gtc',
    jsonify = True)
    print('Trade to buy sent')
    #TODO Check for Status of Trade
    u.time_wait(15)
    print(order)

def sell_crypto (trading_asset, trade_exposure):
    order = r.orders.order_sell_crypto_by_price(
    symbol = trading_asset,
    amountInDollars = float(trade_exposure),
    timeInForce='gtc',
    jsonify = True)
    print('Trade sent to sell')
    #TODO check for status of Trade
    u.time_wait(15)
    print(order)


"""Limit Orders"""

def limit_crypto_buy (trading_asset, trade_exposure, ladder=True):
    if ladder == True:
        #Cancel Orders that are left over from last ladder 
        r.orders.cancel_all_crypto_orders() 
        u.time_wait(5)
        amount = amount_calc_buy(trade_exposure)
        print('Amount', amount)
    #Get Price & Submit Limit Order
    average_btc_price = c.Average_Price_Crypto_Call() #TODO get robin hood market bid ask spread instead
    btc_price = average_btc_price.get_btc()
    order = r.orders.order_buy_crypto_limit_by_price(
        symbol = trading_asset,
        amountInDollars = float(amount),
        limitPrice = (float(btc_price) + float(100)),
        timeInForce = 'gtc',
        jsonify = True)
    print('Limit Placed')
    print(order)
    order_id = order['id']
    #Check Order for Settlment.  If Order Clears -> Throw Ladder.  If order Cancels Throw Cancel Flag. Else Loop
    while True:
        order_check = r.orders.get_crypto_order_info(order_id)
        if order_check['state'] == 'filled':
            print('Trade Filled')
            if ladder == True:
                sell_ladder(amount, trading_asset, on=ladder)
            return 0
        if average_btc_price.get_btc() - float(order_check['price']) > 200: #TODO do % of crypto not bTC
            r.orders.cancel_crypto_order(order_id)
            print(
            "Cancelling Now, the current order price was",
            order_check['price'], 
            "and the current btc price was", 
            average_btc_price.get_btc()
            )
            return 1

        else:
            print('Not setteld as of yet, still spinning')
            u.time_wait(15)



def limit_crypto_sell (trading_asset, trade_exposure, ladder=True):
    r.orders.cancel_all_crypto_orders() #cancel pending trades
    print('Cancel')
    u.time_wait(5)
    #TODO 2 is BTC 1 is ETHE and 3 is DOGE make this passable from selector
    amount = amount_calc_sell(trade_exposure, trading_asset)
    print('amount', amount)
    #Cancel orders from pervious uncleared ladder
    btc_price = c.Average_Price_Crypto_Call().get_btc()
    print(btc_price)
    order = r.orders.order_sell_crypto_limit_by_price(
        symbol = trading_asset,
        amountInDollars = (float(amount)),
        limitPrice = (float(btc_price) - float(100)), #TODO use robin Hood API 
        timeInForce = 'gtc',
        jsonify = True)
    print('Limit Placed')
    print(order)
    order_id = order['id']
    while True:
        order_check = r.orders.get_crypto_order_info(order_id)
        if order_check['state'] == 'filled':
            print('Trade Confirmed')
            if ladder ==True:
                buy_ladder(amount, trading_asset, on=ladder)
            return 0
        if (float(order_check['price'])) - (c.Average_Price_Crypto_Call().get_btc()) > 200:
            r.orders.cancel_crypto_order(order_id)
            print('Cancelling Now')
            return 1
        else:
            print('Not setteld as of yet, still spinning')#update with a call
            u.time_wait(15)
            

"""Trade amount balance calculators"""
def amount_calc_buy (trade_exposure):
    cash = r.profiles.load_account_profile(info='portfolio_cash')
    if float(cash) > float(trade_exposure):
        amount = float(trade_exposure)
    else:
        amount = (float(cash) - 20) 
    return amount

def amount_calc_sell (trade_exposure, trading_asset):
    position = r.crypto.get_crypto_positions()
    bit_quote = r.crypto.get_crypto_quote(symbol=trading_asset)
    current_mv_holdings = (float(bit_quote['bid_price']) * float(position[2]['quantity'])) 
    if current_mv_holdings > float(trade_exposure):
        amount = float(trade_exposure)
    else:
        amount = float(current_mv_holdings) - float(current_mv_holdings * 0.005)
    return amount


#Ladder trading options

def sell_ladder (amount, trading_asset, on=True):
    if on== False:
        return "Ladder off"
    else:
        ladder_btc_price = c.Average_Price_Crypto_Call().get_btc() + 170 #TODO Use robin Hood Market Call
        amount_per_trade = amount * 0.1
        for i in range(3):
            print(f'Order  {i+1}')
            r.orders.order_sell_crypto_limit_by_price(
            symbol = trading_asset,
            amountInDollars = amount_per_trade,
            limitPrice = ladder_btc_price,
            timeInForce = 'gtc',
            jsonify = True)
            ladder_btc_price += 170
        print('Ladder')




def buy_ladder (amount, trading_asset, on=True): 
    if on == True:
        ladder_btc_price = c.Average_Price_Crypto_Call().get_btc() - 170 #TODO Use robin Hood Market Call
        amount_per_trade = amount * 0.1
        for i in range(3):
            print(f'Order  {i+1}')
            r.orders.order_buy_crypto_limit_by_price(
            symbol = trading_asset,
            amountInDollars = amount_per_trade,
            limitPrice = ladder_btc_price,
            timeInForce = 'gtc',
            jsonify = True)
            ladder_btc_price -= 170
        print("Ladder")




        




    
 
 
 

