import Utility as u
import class_list as c


def func_11210 (flag):
    """BTC CROSS EMA SHORT NO-ATR"""

    print('Class Initializer Here. See Func_11210 Details')
    fast = c.EMA_Api_Call().load_ema('btc', '15m',12)
    slow = c.EMA_Api_Call().load_ema('btc', '15m', 26)
    strategy = c.Cross_Over(fast.ema_call_api(), slow.ema_call_api())



    while True:
        fast_ema = fast.ema_call_api()
        slow_ema = slow.ema_call_api()
        strategy.fast_leg = fast_ema
        strategy.slow_leg = slow_ema

        if type(fast_ema) and type(slow_ema) == float or int:
            print('API sucess')
        else:
            print('API Fail, readjusting')
            u.time_wait(16) 
            func_11210(flag)

        print(f"Market Flag {strategy.market_flag()} \n Fast Leg  {strategy.fast_leg} \n Slow Leg {strategy.slow_leg} Delta  {(strategy.fast_leg - strategy.slow_leg)}")

        if flag == 1 and strategy.market_flag() == 1:
            u.time_wait(15)
            return -1

        if flag == -1 and strategy.market_flag() == -1:
            u.time_wait(15)
            return 1
        u.time_wait(16)


def func_11211 (flag):
    """BTC THREE EMA CROSS EMA"""
    flag = flag
    print('Class Initializer Here, See Func 1121 details')
    fast = c.EMA_Api_Call().load_ema('btc', '15m',7)
    middle = c.EMA_Api_Call().load_ema('btc', '15m', 14)
    slow = c.EMA_Api_Call().load_ema('btc', '15m', 21)
    strategy = c.Cross_Over(fast.ema_call_api(), slow.ema_call_api(), middle.ema_call_api())

    while True:
        fast_ema = fast.ema_call_api()
        slow_ema = slow.ema_call_api()
        middle_ema = middle.ema_call_api()
        strategy.fast_leg = fast_ema
        print(strategy.fast_leg)
        strategy.middle_leg = middle_ema
        print(strategy.middle_leg)
        strategy.slow_leg = slow_ema
        print(strategy.slow_leg)

        if type(strategy.middle_leg) and type(strategy.slow_leg) and type(strategy.fast_leg) == float or int:
            print('API sucess')
        else:
            print('API Fail, readjusting')
            u.time_wait(16) 
            func_11211(flag)

        try:
            print(f" The current strategy flag is {strategy.market_flag()} \n 'Fast Leg', {strategy.fast_leg} \n 'Middle Leg', {strategy.middle_leg} 'Slow Leg', {strategy.slow_leg} \n 'Delta Fast/Middle' , {(strategy.fast_leg - strategy.middle_leg)} \n  'Delta Middle/Slow', {strategy.middle_leg - strategy.slow_leg} ")

            if flag == 1 and strategy.market_flag() == 1:
                return -1
                #BUY

            if flag == -1 and strategy.market_flag() == -1:
                return 1
                #Sell

            u.time_wait(16) 
        except:
            print('error recall')
            u.time_wait(15)