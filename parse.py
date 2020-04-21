import requests
import json
import math
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
    start_p = str(trades[0][3])
    end_p = str(trades[len(trades) - 1][3])
    rize = float(end_p) - float(start_p)
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
    if lim_min <= sum_buy and lim_max >= sum_buy and lim_min <= sum_sell and lim_max >= sum_sell:
        print('+++++++++++++')
        return [sum_buy, sum_sell, buy_persent, sell_persent,time.time(),start_p,end_p,rize]
    else:
        return None


def create_msg(list):
    msq = None
    if list != None:
        buy = str(list[0])
        sell = str(list[1])
        rize = str(list[7])
        msq = '🕑 ' + str(datetime.datetime.now().time()) + '  🏛 ' + conf_menu.list_conf[0] + '\n🔹BUY ' + buy[
                                                                                                            :11] + ' btc/1min\n🔻SELL ' + sell[
                                                                                                                                          :11] + ' btc/1min\n💲'+list[5][:6]+'   ➡   💲'+list[6][:6]+' ('+rize[0:5]+'$)\n🔹' + str(
            list[2]) + ' %                   🔻' + str(list[3]) + ' %'
    return msq


def create_statictic(list):
    msg = '🔸🔸🔸🔸'+conf_menu.list_conf[0]+'🔸🔸🔸🔸\n🔹🔺🔹🔺'+conf_menu.list_conf[1]+'/USD🔺🔹🔺🔹\n'
    for l in list :
        if l != None:
            buy = str(l[0])
            sell = str(l[1])
            rize = str(list[7])
            msg += '🕑 '+str(l[4])+'  🏛 '+conf_menu.list_conf[0]+'\n🔹BUY '+buy[:11]+' btc/1min\n🔻SELL '+sell[:11]+' btc/1min\n💲'+list[5][:6]+'   ➡   💲'+list[6][:6]+'('+rize[0:5]+'$)\n🔹'+str(l[2])+' %                   🔻'+str(l[3])+' %\n'
    return msg
