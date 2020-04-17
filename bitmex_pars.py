import requests
import json

buff_id = 0


def get_volume24(coin):
    coin = coin.upper()
    url = 'https://www.bitmex.com/api/v1/instrument?symbol=' + coin + '&count=-1&reverse=true'
    response = requests.get(url)
    trades = json.loads(response.text)
    vol = trades[0].get('volume24h')
    return "🔹Daily volume " + coin + " :" + str(vol)


def get_trades(coin, limit, l_price):
    global buff_id
    coin = coin.upper()
    url = 'https://www.bitmex.com/api/v1/trade?symbol=' + coin + '&count=1&reverse=true'
    response = requests.get(url)
    trades = json.loads(response.text)
    print(trades)
    time = trades[0].get('timestamp')[0:10] + " " + trades[0].get('timestamp')[11:-1]
    type = trades[0].get('side')
    id = trades[0].get('trdMatchID')
    ammount = float(trades[0].get('size'))#*float(trades[0].get('price'))
    price = trades[0].get('price')
    symbol = trades[0].get('symbol')
    return generate_replty(limit, l_price, time, ammount, price, type, id, symbol)


def trade_for_the_period(symbol, st_date, end_date,inerval):
    response = requests.get(
        'https://www.bitmex.com/api/v1/trade/bucketed?binSize='+inerval+'&partial=false&symbol=' + symbol + '&reverse=false&startTime=' + st_date + '&endTime=' + end_date)
    trades = json.loads(response.text)
    print(symbol)
    info = []
    for trade in trades:
        time = trade.get('timestamp')
        time_res = time[0:10]+" "+time[11:-5]
        openT = trade.get('open')
        max_price = trade.get('high')
        min_price = trade.get('low')
        close = trade.get('close')
        volume = trade.get('volume')
        count_trades = trade.get('trades')
        info.append([time_res,openT,max_price,min_price,close,volume,count_trades,symbol])
    return info


def avg_ammount(trades):
    sum = 0
    for trade in trades:
        sum += trade.get('volume')
    return sum / len(trades)


def generate_replty(lim_amm, lim_pri, time, ammount, price, type, id, symbol):
    global buff_id
    if id != buff_id:
        buff_id = id
        if (lim_amm <= ammount and lim_pri <= price):
            if type == 'Buy':
                return "🕐 " + str(time) + "\n📊 BUY\n➡ ammount :" + str(
                    ammount) + " $\n🔷 " + symbol + "\n💰 price " + str(price)
            else:
                return "🕐 " + str(time) + " \n📊 SEL\n➡ ammount :" + str(
                    ammount) + " $\n🔷 " + symbol + "\n💰 price " + str(price)
        else:
            return 'none'
    else:
        buff_id = id
        return 'none'
