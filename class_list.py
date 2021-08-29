from Utility import time_wait
import requests
import time
import Returns as rt
import pyotp
import os
from dotenv import load_dotenv
import robin_stocks.robinhood as r
import ObjectAssembly as o
from twilio.rest import Client


load_dotenv()

class User:

    def __init__ (self, name, phone, sid = os.getenv("TWILIO_SID"), token = os.getenv("TWILIO_TOKEN") ):
        self.name = name
        self.phone = '+' + phone
        self.twilio_phone = '+13347588562'
        self.sid = sid
        self.token = token
        self.client = Client(self.sid , self.token)

    def message_send (self, txt):
        message = self.client.messages.create(
            body=f'Hello {self.name}. EMA Cross Signal {txt} ',
            from_ = self.twilio_phone,
            to = self.phone)
        print(message.sid)

    def messeage_recieve(self):
        pass
         

    def mfa_code(self):
        if self.name == 'mike':
            totp = pyotp.TOTP(os.getenv('PYTOP_APP'))
        if self.name == 'steve':
            totp = pyotp.TOTP(os.getenv('DAD_PYTOP_APP'))
        mfa_code_now = totp.now()
        return mfa_code_now

    def connect_to_RobinHood(self, mfa_code_now): #Console Statment 1
        if self.name == 'mike':
            username = os.getenv('USERNAME')
            password = os.getenv('PASSWORD')
        if self.name == 'steve':
            username = os.getenv('DAD_USERNAME')
            password = os.getenv('DAD_PASSWORD')
        login = r.login(username, password, mfa_code = mfa_code_now)
        user_profile = r.profiles.load_account_profile()
        assert type(user_profile) == dict
        print(rt.connect_to_RobinHood_statment.format(
        fname = self.name,
        profile_time = time.asctime(time.localtime(time.time())),
        profile_acct = user_profile['account_number'],
        profile_cash = user_profile['portfolio_cash']))
        
        return login


    def logging_off_Robinhood(self, position=True): # Console Statment 2

        if position is True:
            ending_str = 'Holding'
        
        else:
            ending_str = 'Not Holding'
        
        user_profile = r.profiles.load_account_profile()
        r.authentication.logout()
        print(rt.logging_off_RobinHood__statment.format(
        profile_cash = user_profile['portfolio_cash'],
        position = ending_str))

    def __repr__ (self):
        pass
        
#----------------------------------------------------------------------------------------------------------------------
class Taapi:

    def __init__ (self):
        self.Auth_Key = os.getenv('taAPI_Auth')
        self.url = os.getenv('URL')


class Test(Taapi):
    def __init__(self, value):
        self.value = value

class Average_Price_Crypto_Call:

    """Average Price of the past 1min candle stick"""

    def __init__ (self, Auth_Key=(os.getenv('taAPI_Auth')), url=(os.getenv('URL'))):
        self.Auth_Key = Auth_Key
        self.url = url
    

    def get_btc (self):
        #average price of last BTC/USDT Last 1m candle
        btc_string = f"https://api.taapi.io/avgprice?secret={self.Auth_Key}&exchange=binance&symbol=BTC/USDT&interval=1m"

        response = requests.get(btc_string)
        if response.status_code != 200:
            time_wait(15)
            self.get_btc()
        else:
            assert response.status_code == 200
        btc_price_json = response.json()
        return (round(btc_price_json['value'],2))

    
class RSI_Call:

    def __init__ (self, Auth_Key=(os.getenv('taAPI_Auth')), url=(os.getenv('URL'))):
        self.Auth_Key = Auth_Key
        self.url = url
    
    def load_rsi (self, asset, interval, timeperiod):
        self.ema_history = []
        self.endpoint = (self.url + 'ema')
        self.asset = asset
        assert(type(asset)) == str
        self.interval = interval
        assert(type(interval)) == str
        self.timeperiod = timeperiod
        assert(type(timeperiod)) == int
        self.params = {
            'secret': self.Auth_Key,
            'exchange': 'binance',
            'symbol' : (self.asset + '/USDT'),
            'interval' : self.interval,
            'optInTimePeriod' : self.timeperiod, 
        }
  
        return self



class EMA_Api_Call(Taapi):
    
    def __init__ (self, Auth_Key=(os.getenv('taAPI_Auth')), url=(os.getenv('URL'))):
        self.Auth_Key = Auth_Key
        self.url = url

    

    def load_ema (self, asset, interval, timeperiod):
        """
        Current Symbol 'COIN'/USDT.  Current Exchange is binance. See https://taapi.io/indicators/exponential-moving-average/ for Param Details 
        """
        
        self.ema_history = []
        self.endpoint = (self.url + 'ema')
        self.asset = asset
        assert(type(asset)) == str
        self.interval = interval
        assert(type(interval)) == str
        self.timeperiod = timeperiod
        assert(type(timeperiod)) == int
        self.params = {
            'secret': self.Auth_Key,
            'exchange': 'binance',
            'symbol' : (self.asset + '/USDT'),
            'interval' : self.interval,
            'optInTimePeriod' : self.timeperiod, 
        }
  
        return self
       
    def ema_call_api (self):
        """
        Calls EMA API and Stores in History Queue
        """

        response = requests.get(url = self.endpoint, params = self.params)
        if response.status_code != 200:

            time_wait(15)
            self.ema_call_api()

        else:

            assert response.status_code == 200
            ema_json = response.json()
            self.ema_value = ema_json['value']
            self.ema_history.append(self.ema_value)
            if len(self.ema_history) > 10:
                self.ema_history.pop(-1)

            return self.ema_value
        
    def ema_queue (self):

        "Created in case later strategies require a past ema values, looking for trend etc..."

        for ema in self.ema_history:
            print(ema)
        

    def ema__repr__ (self):

        "Current State of the EMA Class"

        repr = "Exchange Binance \n Symbol {} \n Interval {} \n opInTimePeriod {} \n Current EMA Value {} \n Current EMA Queue {}".format(self.asset, self.interval, self.timeperiod, self.ema_value, self.ema_history) 

        return repr

class RSI_API:
    "Future RSI API Call"
    pass

        
class Volatility_API:

    "Pull of ATR Volatility. https://taapi.io/indicators/average-true-range/"   

    def __init__ (self):

        self.Auth_Key = os.getenv('taAPI_Auth')
        self.url = os.getenv('URL')
        self.indicator = 'atr'
        self.endpoint = self.url + self.indicator
        self.exchange = 'binance'
        self.atr_history = []

    def load_volatility (self, object, timeperiod=None):

        "Load Object Like EMA_API_Call or RSI_call. Overide Timeperiod if object.timeperiod is not desired"

        self.interval = object.interval
        self.asset = object.asset
        if timeperiod == None:
            self.timeperiod = object.timeperiod
        else:
            self.timeperiod = timeperiod

        self.params = {
        'secret': self.Auth_Key,
        'exchange': 'binance',
        'symbol' : (self.asset + '/USDT'),
        'interval' : object.interval,
        'opInTimePeriod' : self.timeperiod, 
        }
        return self


    def volatility_call_api (self):

        "Return ATR and Loads ATR into Volatility Queue"

        response = requests.get(url = self.endpoint, params = self.params)

        if response.status_code != 200:
            time_wait(15)
            self.volatility_call_api()

        else:
            atr_json = response.json()
            self.atr_value = atr_json['value']
            self.atr_history.append(self.atr_value)
            if len(self.atr_history) > 10:
                self.atr_history.pop(-1)

            return self.atr_value


    def volatility_queue (self):

        "Created in case later strategies require a past ema values, looking for trend etc..."

        for self.atr_value in self.atr_history:

            print("Queue", self.atr_value)

        
    def volatility__repr__ (self):

        " Current State of the EMA Class "

        repr = "Exchange Binance \n Symbol {} \n Interval {} \n opInTimePeriod {} \n Current EMA Value {} \n Current EMA Queue {}".format(self.asset, self.interval, self.timeperiod, self.atr_value, self.atr_history) 
        
        return repr

#----------------------------------------------------------------------------------------------------------------------

class Cross_Over:

    "Flags for cross overs when using moving averages, Optional volatility condition.  Volatility is set to take in a Volatility Number.  Set to False to Ignore"

    def __init__ (self, fast_leg, slow_leg, middle_leg):

        self.fast_leg = fast_leg
        self.slow_leg = slow_leg
        self.middle_leg = middle_leg
        


    def market_flag (self):
        "Looks for Cross Over and Returns Buy or Sell Flag"

        if self.middle_leg == None:
                print('TWO-EMA-Cross')
                if self.fast_leg > self.slow_leg + 15: #TODO Research that
                    return 1
                elif self.slow_leg > self.fast_leg + 15:
                    return -1
                else:
                    return 0
        else:
            print('THREE-EMA-Cross')
            if self.fast_leg > self.middle_leg + 12  > self.slow_leg + 12: #TODO Research that
                return 1
            elif self.slow_leg > self.middle_leg + 12 > self.fast_leg + 12:
                return -1
            else:
                return 0


    
        

    


        







