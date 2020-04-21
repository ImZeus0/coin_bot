import requests
import json
import math
import xlsx_writer
import conf_menu
import datetime

buff_id = 0


def get_trades(symbol, date,lim_min,lim_max):
    res_trades = []
    jump = datetime.timedelta(minutes=1)
    startTime = datetime.datetime.now() - datetime.timedelta(minutes=date)
    buffTime = startTime + jump
    while buffTime != datetime.datetime.now():
        if buffTime < datetime.datetime.now():
            print(startTime, buffTime)
            ms_s_time = int(startTime.timestamp())
            ms_b_time = int(buffTime.timestamp())
            url = 'https://api-pub.bitfinex.com/v2/trades/t' + symbol + 'USD/hist?limit=10000&start=' + str(
                ms_s_time) + '000&end=' + str(ms_b_time) + '000&sort=-1'
            response = requests.get(url)
            list = json.loads(response.text)
            res_trades.append(sum_coin(list, lim_min, lim_max))
            startTime = buffTime
            buffTime = startTime + jump
        else:
            break
    print(res_trades)
    return create_statictic(res_trades)


def trades(symbol, lim_max, lim_min):
    startTime = datetime.datetime.now() - datetime.timedelta(minutes=1)
    buffTime = datetime.datetime.now()
    print(startTime.time())
    print(buffTime.time())
    ms_s_time = int(startTime.timestamp())
    ms_b_time = int(buffTime.timestamp())
    url = 'https://api-pub.bitfinex.com/v2/trades/t' + symbol + 'USD/hist?limit=10000&start=' + str(
        ms_s_time) + '000&end=' + str(ms_b_time) + '000&sort=-1'
    response = requests.get(url)
    list = json.loads(response.text)
    return create_msg(sum_coin(list, lim_max, lim_min))


def sum_coin(trades, lim_max, lim_min):
    sum_buy = 0
    sum_sell = 0
    time = 0
    for t in trades:
        if float(t[2]) > 0:
            sum_buy += math.fabs(float(t[2]))
        elif float(t[2]) < 0:
            sum_sell += math.fabs(float(t[2]))
        else:
            pass
        time = datetime.datetime.fromtimestamp(t[1] / 1000)
    buy_persent = int((100 * sum_buy) / (sum_sell + sum_buy))
    sell_persent = int((100 * sum_sell) / (sum_sell + sum_buy))
    print(sum_buy, "$")
    print(sum_sell, "$")
    if lim_min < sum_buy and lim_max > sum_buy and lim_min < sum_sell and lim_max > sum_sell:
        print('+++++++++++++')
        return [sum_buy, sum_sell, buy_persent, sell_persent,time.time()]
    else:
        return None


def create_msg(list):
    msq = None
    if list != None:
        buy = str(list[0])
        sell = str(list[1])
        msq = '🕑 ' + str(datetime.datetime.now().time()) + '  🏛 ' + conf_menu.list_conf[0] + '\n🔹BUY ' + buy[
                                                                                                            :11] + ' btc/1min\n🔻SELL ' + sell[
                                                                                                                                          :11] + ' btc/1min\n🔹' + str(
            list[2]) + ' %                   🔻' + str(list[3]) + ' %'
    return msq


def create_statictic(list):
    msg = '🔸🔸🔸🔸'+conf_menu.list_conf[0]+'🔸🔸🔸🔸\n🔹🔺🔹🔺'+conf_menu.list_conf[1]+'/USD🔺🔹🔺🔹\n'
    for l in list :
        if l != None:
            buy = str(l[0])
            sell = str(l[1])
            msg += '🕑 '+str(l[4])+'  🏛 '+conf_menu.list_conf[0]+'\n🔹BUY '+buy[:11]+' btc/1min\n🔻SELL '+sell[:11]+' btc/1min\n🔹'+str(l[2])+' %                   🔻'+str(l[3])+' %\n'
    return msg
