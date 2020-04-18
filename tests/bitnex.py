import json
import requests
import datetime


#https://www.bitmex.com/api/v1/trade?symbol=XBTUSD&count=1000&reverse=true&startTime=2020-04-17T23%3A33Z&endTime=2020-04-17T23%3A38Z
#https://www.bitmex.com/api/v1/trade?symbol=XBTUSD&count=1000&reverse=true&startTime=2020-04-17T20%3A16Z&endTime=2020-04-17T20%3A21Z


def parse(symbol, date, rate):
    res_trades = []
    jump = datetime.timedelta(minutes=5)
    startTime = datetime.datetime.now() - datetime.timedelta(minutes=date)
    buffTime = startTime + jump
    while buffTime != datetime.datetime.now():
        if buffTime < datetime.datetime.now():
            print(startTime.time(),startTime.minute,buffTime)
            arr = str(startTime).split(':')
            s_m = arr[1]
            arr1 = str(buffTime).split(':')
            e_m = arr1[1]
            url = 'https://www.bitmex.com/api/v1/trade?symbol='+symbol+'USD&count=1000&reverse=true&startTime='+str(startTime.date())+'T'+str(startTime.time().hour)+'%3A'+s_m+'Z&endTime='+str(buffTime.date())+'T'+str(buffTime.time().hour)+'%3A'+e_m+'Z'
            print(url)
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


parse("XBT",50 ,1000)
