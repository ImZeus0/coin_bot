import requests
import json
import datetime
import conf_menu

buff_id = 0
#https://www.bitmex.com/api/v1/trade?count=100&reverse=false&startTime=2020-04-04%2010%3A10%3A10&endTime=2020-04-04%2010%3A10%3A20
def get_trades(symbol,min_lim,max_lim):
    UTC = datetime.timedelta(hours=3)
    startTime = datetime.datetime.now() - datetime.timedelta(seconds=10)-UTC
    buffTime = datetime.datetime.now()-UTC
    print(startTime, buffTime)
    arr = str(startTime).split(':')
    s_m = arr[1]
    s_s = arr[2][:2]
    arr1 = str(buffTime).split(':')
    e_m = arr1[1]
    e_s = arr1[2][:2]
    print(s_s,e_s)
    url = 'https://www.bitmex.com/api/v1/trade?symbol=' + symbol + 'USD&count=1000&reverse=true&startTime=' + str(
        startTime.date()) + 'T' + str(startTime.time().hour) + '%3A' + s_m + '%3A' + s_s+'&endTime=' + str(
        buffTime.date()) + 'T' + str(buffTime.time().hour) + '%3A' + e_m + '%3A' + e_s
    print(url)
    response = requests.get(url)
    list = json.loads(response.text)
    print(list)
    return create_msg(format(list,min_lim,max_lim))

def format(trades,min_lim,max_lim):
    res = []
    for t in trades:
        volume = int(t.get('size'))
        print(volume)
        if min_lim<volume<max_lim:
            price = float(t.get('price'))
            type = t.get('side')
            time = t.get('timestamp')
            res +=[[time[11:19],volume,price,type]]
    return res

def create_msg(lists):
    msg = ''
    for list in lists:
        msg += '🕑 '+list[0]+'  🏛 '+conf_menu.list_conf[0]+'\n🔹'+str(list[3])+'  💲 '+str(list[2])+'  💰 '+str(list[1])+'\n'
    return msg


def trade_for_the_period(symbol, date, rate):
    res_trades = []
    UTC = datetime.timedelta(hours=3)
    jump = datetime.timedelta(minutes=1)
    startTime = datetime.datetime.now() - datetime.timedelta(minutes=date)-UTC
    buffTime = startTime + jump
    while buffTime != datetime.datetime.now()-UTC:
        if buffTime < datetime.datetime.now()-UTC:
            #print(startTime,buffTime)
            arr = str(startTime).split(':')
            s_m = arr[1]
            arr1 = str(buffTime).split(':')
            e_m = arr1[1]
            url = 'https://www.bitmex.com/api/v1/trade?symbol='+symbol+'USD&count=1000&reverse=true&startTime='+str(startTime.date())+'T'+str(startTime.time().hour)+'%3A'+s_m+'Z&endTime='+str(buffTime.date())+'T'+str(buffTime.time().hour)+'%3A'+e_m+'Z'
            #print(url)
            response = requests.get(url)
            list = json.loads(response.text)
            #print(list)
            for l in list:
                volume = l.get('size')
                type = l.get('side')
                price = l.get('price')
                if float(volume)  >= rate:
                    time = l.get('timestamp')
                    res_trades.append([time[11:19],symbol,volume,price,type])
            startTime = buffTime
            buffTime = startTime+jump
        else:
            break
    return create_statictic(res_trades)

def create_statictic(list):
    msg = '🔸🔸🔸🔸'+conf_menu.list_conf[0]+'🔸🔸🔸🔸\n🔹🔺🔹🔺'+conf_menu.list_conf[1]+'/USD🔺🔹🔺🔹\n'
    for l in list :
        if l[4] == 'Sell':
            msg += '🕐 '+l[0][0:9]+'  🅰️ '+str(l[2])+' $\n🔻'+str(l[4])+'                💸'+str(l[3])+'\n'
        else:
            msg += '🕐 ' + l[0][0:9] + '  🅰️ ' + str(l[2]) + ' $\n🔹' + str(l[4]) + '                💸' + str( l[3]) + '\n'
    return msg


