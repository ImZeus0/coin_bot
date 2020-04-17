import requests
import json
import time
from datetime import datetime
import datetime as DT
buff_id = 0


def get_trades(coin, lim):
    coin = coin.upper()
    url = 'https://api.binance.com/api/v3/trades?symbol=' + coin + 'USDT'
    response = requests.get(url)
    trades = json.loads(response.text)
    time = datetime.fromtimestamp(int(int(trades[0].get('time')) / 1000))
    price = trades[0].get('price')
    symbol = coin
    id = trades[0].get('id')
    if trades[0].get('isBuyerMaker') == True:
        type = 'Buy'
    else:
        type = 'Sell'
    ammount = float(trades[0].get('qty')) * float(price)
    return generate_replty(lim, time, float(ammount), float(price), type, id, symbol)

def trade_for_period(symbol,st_date,end_date,interval):
    st_date = DT.datetime.fromisoformat(st_date)
    st_date = st_date.timestamp()
    end_date = DT.datetime.fromisoformat(end_date)
    end_date = end_date.timestamp()
    url = 'https://api.binance.com/api/v3/klines?symbol='+symbol+'USDT&interval='+interval+'&startTime='+str(int(st_date))+'000&endTime='+str(int(end_date))+'000'
    response = requests.get(url)
    trades = json.loads(response.text)
    print(response.text)
    info =[]
    for trade in trades:
        time = datetime.fromtimestamp(int(int(trade[0])/1000))
        open = trade[1][:-6]
        max_price = trade[2][:-6]
        min_price = trade[3][:-6]
        close = trade[4][:-6]
        volume = trade[5][:-6]
        count_trades = trade[8]
        info.append([time,open,max_price,min_price,close,volume,count_trades,symbol])
    return info

def generate_replty(lim_amm, time, ammount, price, type, id, symbol):
    global buff_id
    if id != buff_id:
        buff_id = id
        if (lim_amm <= ammount):
            if type == 'Buy':
                return "🕐 " + str(time) + "\n\n🔷 "+symbol+"\n📊 BUY\n➡ ammount :" + str(
                    ammount) + " $\n💰 price " + str(price)
            else:
                return "🕐 " + str(time) + "\n\n🔷 " + symbol + "\n📊 SELL\n➡ ammount :" + str(
                    ammount) + " $\n💰 price " + str(price)
        else:
            return 'none'
    else:
        buff_id = id
        return 'none'

