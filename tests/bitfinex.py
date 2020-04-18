
import json
import requests
import datetime


def parse(symbol, date, rate):
    res_trades = []
    jump = datetime.timedelta(minutes=5)
    startTime = datetime.datetime.now() - datetime.timedelta(minutes=date)
    buffTime = startTime + jump
    while buffTime != datetime.datetime.now():
        if buffTime < datetime.datetime.now():
            print(startTime,buffTime)
            ms_s_time = int(startTime.timestamp())
            ms_b_time = int(buffTime.timestamp())
            url = 'https://api-pub.bitfinex.com/v2/trades/t'+symbol+'USD/hist?limit=10000&start='+str(ms_s_time)+'000&end='+str(ms_b_time)+'000&sort=-1'
            response = requests.get(url)
            list = json.loads(response.text)
            print(list)
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


parse("BTC",30 ,1000)
