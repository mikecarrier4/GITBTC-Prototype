import Utility as u
import class_list as c
import engine as e
import robin_stocks.robinhood as r
from dotenv import load_dotenv






if __name__ == '__main__':
    user = input('Name ')
    user_phone = '18153557345'
    c.User(user, user_phone)
    key = input("Enter Key")
    amount = input("Enter Amount")
    #TODO Check for funds function
    michael = c.User(user, user_phone)
    mfa = michael.mfa_code()
    login = michael.connect_to_RobinHood(mfa)
    trading_asset = '3d961844-d360-45fc-989b-f6fca761d511' #update this
    start_position = e.last_trade(trading_asset, flag=1) # DAD Right Here 
    flag = start_position
    e.engine(flag, key, amount)