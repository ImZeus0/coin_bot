import json
import requests
import datetime

def parse(symbol,date):
    delta = datetime.timedelta(minutes=date)
    startTime = datetime.datetime.now() - delta
    ms_s_time = int(startTime.timestamp())
    ms_e_time = int(datetime.datetime.now().timestamp())
    print(ms_s_time)
    print(ms_e_time)
    url = 'https://www.binance.com/api/v3/aggTrades?symbol='+symbol+'USDT&startTime='+str(ms_s_time)+'000&endTime='+str(ms_e_time)+'000&limit=1000'
    response =requests.get(url)
    list = json.loads(response.text)
    print(list)


parse("BTC",30)