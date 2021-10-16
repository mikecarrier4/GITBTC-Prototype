import Utility as u
import class_list as c
import engine as e
import robin_stocks.robinhood as r
from dotenv import load_dotenv
import sys 
import os, signal
import DB as db






if __name__ == '__main__':

    sys_string = str(sys.argv[1:])

    crypto_dict = {
        'Bitcoin' : ['BTC', '3d961844-d360-45fc-989b-f6fca761d511'],
        'Ethereum' : ['ETH', None],
        'Doge' : ["DODG", None]
    }

    class Bootstrap_Crypto:

        def __init__ (self, dict):
            self.dict = dict
            self.phone = db.User().user_phone(dict['pin'])
            self.Algo_User = c.User(dict['fn'], self.phone, dict['a'], dict['b'], dict['c'])
            self.strategy_pin = dict['Crypto'] + dict['Duration'] + dict['Strategy']
            self.amount = float(dict['d'])
            self.pin = dict['pin']
        
        def get_RH_token (self):
            self.token = self.Algo_User.connect_to_RobinHood()
            return self.token

        def get_strategy_pin (self):
            self.strategy_pin = self.dict['Crypto'] + self.dict['Duration'] + self.dict['Strategy']
            return self.strategy_pin
        
        def get_pid_id(self):
            return os.getpid()
    



            
    #TODO research session args cache system
    sys_string = sys_string.strip('["<SecureCokkieSession ').strip('>"]')
    dict = eval(sys_string)
    print(dict)
    Algo_user = Bootstrap_Crypto(dict)
    Token = Algo_user.get_RH_token()
    #os.kill(44932, signal.SIGTERM)
    """clear dictionary variable args"""
    dict = None
    Strategy_PIN = Algo_user.get_strategy_pin()
    job_id = Algo_user.get_pid_id()
    print(Algo_user.pin)
    user_id = db.User().user_id(Algo_user.pin)
    db.Running_Jobs().insert_job(job_id, Strategy_PIN, user_id)
    start_position = e.last_trade(crypto_dict['Bitcoin'][1], flag=-1)
    e.engine(start_position, '2' , Algo_user.amount, crypto_dict['Bitcoin'][0])
