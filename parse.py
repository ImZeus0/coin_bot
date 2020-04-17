import requests
import json
import math
from datetime import datetime
import datetime as DT
import parse

buff_id = 0

def daily_am(coin):
    coin = coin.upper()
    url = 'https://api-pub.bitfinex.com/v2/tickers?symbols=t'+coin+'USD'
    response = requests.get(url)
    res = json.loads(response.text)
    print(res)
    return 'Daily volume: '+str(res[0][8])


def get_trades(coin, limit, l_price):
    coin = coin.upper()
    url = 'https://api-pub.bitfinex.com/v2/trades/t'+coin+'USD/hist'
    response = requests.get(url)
    symbol = coin
    trades = json.loads(response.text)
    time = datetime.fromtimestamp(int(trades[0][1] / 1000))
    ammount = math.fabs(trades[0][2])*trades[0][3]
    price = trades[0][3]
    id = trades[0][0]
    type = ''
    if trades[0][2] >= 0:
        type = 'BUY'
    else:
        type = 'SELL'
    return generate_replty(limit, l_price, time, ammount, price, type,id,symbol)

def trade_for_the_period(symbol,start_t,end_t,period):
    start_t = datetime.strptime(start_t,'%Y-%m-%d')
    start_t = str(int(start_t.timestamp()))
    end_t = datetime.strptime(end_t, '%Y-%m-%d')
    end_t = str(int(end_t.timestamp()))
    url = 'https://api-pub.bitfinex.com/v2/candles/trade:'+period+':t'+symbol+'USD/hist?start='+start_t+'000&end='+end_t+'000&sort=-1'
    response = requests.get(url)
    trades = json.loads(response.text)
    info = []
    for trade in trades:
        time = datetime.fromtimestamp(int(trade[0] / 1000))
        openT = trade[1]
        max_price = trade[3]
        min_price = trade[4]
        close = trade[2]
        volume = trade[5]
        info.append([time, openT, max_price, min_price, close, volume, symbol])
    return info


def generate_replty(lim_amm, lim_pri, time, ammount, price, type,id,symbol):
    global buff_id
    if id != buff_id:
        buff_id = id
        if (lim_amm <= ammount and lim_pri <= price):
            if type == 'BUY':
                return "🕐 " + str(time) + "\n📊 BUY\n➡ ammount :" + str(ammount) +"\n🔷 "+symbol+"\n💰 price "+str(price)
            else:
                return "🕐 " + str(time) + " \n📊 SEL\n➡ ammount :" + str(ammount) + "\n🔷 "+symbol+"\n💰 price "+str(price)
        else:
            return 'none'
    else:
        buff_id = id
        return 'none'
