import requests
import json
import time
import datetime
import conf_menu
import datetime as DT
buff_id = 0


def get_trades(coin, lim):
    coin = coin.upper()
    url = 'https://api.binance.com/api/v3/trades?symbol=' + coin + 'USDT'
    response = requests.get(url)
    trades = json.loads(response.text)
    time = datetime.datetime.fromtimestamp(int(int(trades[0].get('time')) / 1000))
    price = trades[0].get('price')
    symbol = coin
    id = trades[0].get('id')
    if trades[0].get('isBuyerMaker') == True:
        type = 'Buy'
    else:
        type = 'Sell'
    ammount = float(trades[0].get('qty')) * float(price)
    return generate_replty(lim, time, float(ammount), float(price), type, id, symbol)

def trade_for_period(symbol, date, rate):
    res_trades = []
    jump = datetime.timedelta(minutes=5)
    startTime = datetime.datetime.now() - datetime.timedelta(minutes=date)
    buffTime = startTime + jump
    while buffTime != datetime.datetime.now():
        if buffTime < datetime.datetime.now():
            print(startTime,buffTime)
            ms_s_time = int(startTime.timestamp())
            ms_b_time = int(buffTime.timestamp())
            url = 'https://www.binance.com/api/v3/aggTrades?symbol=' + symbol + 'USDT&startTime=' + str(ms_s_time) + '000&endTime=' + str(ms_b_time) + '000&limit=1000'
            response = requests.get(url)
            list = json.loads(response.text)
            for l in list:
                volume = l.get('q')
                price = l.get('p')
                if float(volume) * float(price) >= rate:
                    print (float(volume) * float(price))
                    print(l)
                    res_trades.append(l)
            startTime = buffTime
            buffTime = startTime+jump
        else:
            break
    return res_trades

def repry_statistic(list):
    msg = ' '
    for l in list:
        volume = int(float(l.get('q'))*float(l.get('p')))
        price = int(float(l.get('p')))
        time = datetime.datetime.fromtimestamp(int(l.get('T')/1000))
        if l.get('m') == True:
            t_type = "BUY"
        else:
            t_type = "SELL"
        msg += 'TIME : '+str(time.time())+' '+conf_menu.list_conf[1]+' '+t_type+' VOLUME : '+str(volume)+' PRICE : '+str(price)+'\n'
    print(msg)
    if msg == ' ':
        return "Совпадений не найдено"
    else:
        return msg
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

def trades(symbol):
    while 1:
        startTime = datetime.datetime.now() - datetime.timedelta(minutes=1)
        buffTime = datetime.datetime.now()
        print(startTime, buffTime)
        ms_s_time = int(startTime.timestamp())
        ms_b_time = int(buffTime.timestamp())
        url = 'https://www.binance.com/api/v3/aggTrades?symbol=' + symbol + 'USDT&startTime=' + str(
            ms_s_time) + '000&endTime=' + str(ms_b_time) + '000&limit=1000'
        response = requests.get(url)
        list = json.loads(response.text)
        print(sum_coin(list))
        time.sleep(60)

def sum_coin(trades):
    sum_buy = 0
    sum_sell = 0
    for t in trades:
        if t.get('M') == True:
            sum_buy += int(float(t.get('q'))*float(t.get('p')))
        elif t.get('M') == False:
            sum_sell += int(float(t.get('q')) * float(t.get('p')))
    return [sum_buy,sum_sell]

trades("BTC")