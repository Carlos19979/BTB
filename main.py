from binance.client import Client
from binance.enums import *
import config
import os
from binance.exceptions import BinanceAPIException, BinanceWithdrawException
from forex_python.bitcoin import BtcConverter

client = Client(config.apiKey,config.apiSecurity)

investVariable = 0.0
limitSell = 0.0
stopLossAlert = 0.0
stopLossSell = 0.0


def menu():
    print()
    print("[0] start Pump bot")
    print("[1] balance")
    print("[2] invest                          ",investVariable,"%")
    print("[3] profits                         ",limitSell,"%")
    print("[4] stop loss alarm                 ",stopLossAlert,"%")
    print("[5] stop loss sell                  ",stopLossSell,"%")
    print("[6] exit")

    

menu()
print()
option = int(input("enter your option: "))
print()

while option != 6:
    if option == 1:
        c = BtcConverter()
        info = client.get_asset_balance('BTC')
        print('your current balance is: ')
        print()
        print('€', round(c.convert_btc_to_cur(float(info['free']),'EUR')))
        print('$', round(c.convert_btc_to_cur(float(info['free']),'USD')))
        print('£', round(c.convert_btc_to_cur(float(info['free']),'GBP')))
                
                
    elif option == 2:
        print()
        investVariable = int(input("enter how much of you balance you want to invest: "))
        print()
        print('you have selected: ',investVariable,'% of your total balance')
    elif option == 3:
        print()
        limitSell = int(input("enter how much profits % you want to make before selling: "))
        print()
        print('your crypto is going to sell at: ',limitSell,'% profits')
    elif option == 4:
        print()
        stopLossAlert = int(input("enter the % when does stop loss  alert triggers: "))
        print()
        print('your alert will trigger once the price goes down: ',stopLossAlert,'%')
    elif option == 5:
        print()
        stopLossSell = int(input("enter the % when does stop loss sell triggers: "))
        print()
        print('your crypto will sell when price is down: ',stopLossSell,'%')
    elif option == 0:
     try: 
                   print()
                   info = client.get_asset_balance('BTC')
                   btcBalance = info['free']
                   res = float(btcBalance)*float(investVariable)/100.0
                   coin = input("select a coin (CAPS ONLY): ")
                   coin +='BTC'
                   fees = client.get_trade_fee(symbol=coin)
                  
                   lastPrice = client.get_symbol_ticker(symbol=coin)
                   lastPriceFloat =  float(lastPrice['price'])
                   quantity = float(round(res/lastPriceFloat))
                   
                   price_limitSell = '{:0.0{}f}'.format(lastPriceFloat+(lastPriceFloat*limitSell/100.0), 8)
                   price_limitLoss = '{:0.0{}f}'.format(lastPriceFloat-(lastPriceFloat*stopLossSell/100.0), 8)
                   price_limitLossAlert = '{:0.0{}f}'.format(lastPriceFloat-(lastPriceFloat*stopLossAlert/100.0), 8)
                   
                   price_strProfits = '{:0.0{}f}'.format(res+(res*limitSell/100.0), 8)
                   price_strLosings = '{:0.0{}f}'.format(res-(res*stopLossSell/100.0), 8)
                   price_strTrigerLosings = '{:0.0{}f}'.format(lastPriceFloat-(lastPriceFloat*stopLossAlert/100.0), 8)
                  
                   buyOrder = client.order_market(
                   symbol=coin,
                   side=client.SIDE_BUY,
                   quantity=quantity)
                   
                   order = client.create_oco_order(
                   symbol=coin,
                   side=client.SIDE_SELL,
                   quantity=quantity,
                   price=price_limitSell,
                   stopPrice=price_limitLoss,
                   stopLimitPrice=price_limitLossAlert,
                   stopLimitTimeInForce=client.TIME_IN_FORCE_GTC)
                   
                   c = BtcConverter()
                   print("[BUY]  Quantity ",quantity," | price: ",lastPrice['price'],'BTC')
                   print("[SELL] Quantity ",quantity," | price: ",price_limitSell,'BTC')
                   print("---------------------------------------------------------------")
                   print("-->[PROFITS]",round(c.convert_btc_to_cur(float(price_strProfits),'EUR'),2),'EUR |',round(c.convert_btc_to_cur(float(price_strProfits),'USD'),2),'USD |',round(c.convert_btc_to_cur(float(price_strProfits),'GBP'),2),'GBP')
                   print("-->[LOSSES]",round(c.convert_btc_to_cur(float(price_strLosings),'EUR'),2),'EUR |',round(c.convert_btc_to_cur(float(price_strLosings),'USD'),2),'USD |',round(c.convert_btc_to_cur(float(price_strLosings),'GBP'),2),'GBP')
                   input()
                   
                  

               
     except BinanceAPIException as e:
                   if(e.message =='Filter failure: MIN_NOTIONAL'):
                       print('account balance is not enought to buy (10 USD) minumum')
                   else:
                       print(e.message)
 
    else:
        print('error')  
    
    print()
    menu()
    print()
    option = int(input("enter your option: "))
