import json
import requests
import datetime

def parse(symbol,date,rate):
    res_trades = []
    jump = datetime.timedelta(minutes=5)
    startTime = datetime.datetime.now() - datetime.timedelta(minutes=date)
    buffTime = startTime+jump
    while buffTime != datetime.datetime.now():
        ms_s_time = int(startTime.timestamp())
        ms_b_time = int(buffTime.timestamp())
        url = 'https://www.binance.com/api/v3/aggTrades?symbol='+symbol+'USDT&startTime='+str(ms_s_time)+'000&endTime='+str(ms_b_time)+'000&limit=1000'
        response =requests.get(url)
        list = json.loads(response.text)
        for l in list:
            volume = l.get('q')
            price = l.get('p')
            if float(volume)*float(price) >= rate:
                res_trades.append(l)


parse("BTC",30)