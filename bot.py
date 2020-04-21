import telebot
import config
import keyboard
import re
import parse
import time
import binance_pars
import bitmex_pars
import conf_menu
import lang

language = 0
flag_stream = True

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    global flag_stream
    bot.send_message(message.chat.id, 'Выберете язык / Choose a language', reply_markup=keyboard.lang_menu())
    conf_menu.list_conf = [' ']
    flag_stream = False


def start_bitmex(m, symbol, lim_max,lim_min):
    global flag_stream
    flag_stream = True
    bot.send_message(m.chat.id, 'Start striming', reply_markup=keyboard.stream_menu_2())
    while flag_stream:
        reply = bitmex_pars.get_trades(symbol,lim_max,lim_min)
        print(reply)
        if reply != None and len(reply)>5:
            bot.send_message(config.chat, reply)
        time.sleep(10)


def start_binance(m, symbol, lim_max,lim_min):
    global flag_stream
    flag_stream = True
    bot.send_message(m.chat.id, 'Start striming', reply_markup=keyboard.stream_menu_2())
    while flag_stream:
        reply = binance_pars.trades(symbol,lim_max,lim_min)
        print(reply)
        if reply != None:
            bot.send_message(config.chat, reply)
        time.sleep(60)


def start_bitfinex(m, symbol, lim_max,lim_min):
    global flag_stream
    flag_stream = True
    bot.send_message(m.chat.id, 'Start striming', reply_markup=keyboard.stream_menu_2())
    while flag_stream:
        reply = parse.trades(symbol, lim_max,lim_min)
        print(reply)
        if reply != None:
            bot.send_message(config.chat, reply[1:])
        time.sleep(60)


@bot.message_handler(commands=['l'])
def set_intr(m):
    try:
        num = m.text.split(' ')
        intr = int(num[1])
        intr1 = int(num[2])
        conf_menu.list_conf.append(intr)
        conf_menu.list_conf.append(intr1)
        bot.send_message(m.chat.id, "Лимит установлен", reply_markup=keyboard.stream_menu_1())
    except Exception as l:
        bot.send_message(m.chat.id, str(l) + ' Некорректный запрос')


@bot.message_handler(commands=['m'])
def date(m):
    try:
        msg = m.text.split(' ')
        match = re.search(r'\d+', msg[1])
        if match:
            if round(float(msg[1])) <= 60 and round(float(msg[1])) >= 1:
                conf_menu.list_conf.append(round(float(msg[1])))
                bot.send_message(m.chat.id, lang.en_amm[conf_menu.lang])
            else:
                bot.send_message(m.chat.id, 'Слишком большое число или слишком маленькое (60 > n > 0)')
        else:
            bot.send_message(m.chat.id, 'Введите число')
    except:
        bot.send_message(m.chat.id, 'Некорректный запрос')


@bot.message_handler(commands=['hist'])
def limit(m):
    mim = m.text.split(' ')
    if len(conf_menu.list_conf) == 3 :
        conf_menu.list_conf.append(float(mim[1]))
        conf_menu.list_conf.append(float(mim[2]))
        print(conf_menu.list_conf[2])
        print(conf_menu.list_conf[3])
        if conf_menu.list_conf[0] == 'binance':
            res = binance_pars.trade_for_period(conf_menu.list_conf[1], conf_menu.list_conf[2],
                                                    conf_menu.list_conf[3],conf_menu.list_conf[4])
            print(res)
            if len(res) < 4000:
                bot.send_message(config.chat, res)
            else:
                bot.send_message(config.chat, res[0:3998] + "\n\nСообщение слишком длинное")
            bot.send_message(m.chat.id,"OK",reply_markup=keyboard.main_menu())
            conf_menu.list_conf = [' ']
        elif conf_menu.list_conf[0] == 'bitfinex':
            res = parse.get_trades(conf_menu.list_conf[1], conf_menu.list_conf[2],
                                                    conf_menu.list_conf[4],conf_menu.list_conf[3])
            print(res)
            if len(res) < 4000:
                bot.send_message(config.chat, res)
            else:
                bot.send_message(config.chat, res[0:3998] + "\n\nСообщение слишком длинное")
            bot.send_message(m.chat.id, "OK", reply_markup=keyboard.main_menu())
            conf_menu.list_conf = [' ']
        elif conf_menu.list_conf[0] == 'bitmex':
            res = bitmex_pars.trade_for_the_period(conf_menu.list_conf[1], conf_menu.list_conf[2],
                                                       conf_menu.list_conf[3])
            print(res)
            if len(res) < 4000:
                bot.send_message(config.chat, res)
            else:
                bot.send_message(config.chat, res[0:3998] + "\n\nСообщение слишком длинное")
            bot.send_message(m.chat.id, "OK", reply_markup=keyboard.main_menu())
            conf_menu.list_conf = [' ']
        else:
            bot.send_message(m.chat.id, 'Некорректный запрос ‼')
    else:
        bot.send_message(m.chat.id, lang.error[conf_menu.lang], reply_markup=keyboard.main_menu())
        conf_menu.list_conf = ['']



@bot.message_handler(content_types=['text'])
def menu(m):
    global language
    if m.text == 'Russian 🇷🇺':
        conf_menu.lang = 0
        bot.send_message(m.chat.id, lang.start[conf_menu.lang], reply_markup=keyboard.main_menu())
    elif m.text == 'Сменить язик' or m.text == 'Change language':
        bot.send_message(m.chat.id, m.text, reply_markup=keyboard.lang_menu())
    elif m.text == 'English 🏴󠁧󠁢󠁥󠁮󠁧󠁿':
        conf_menu.lang = 1
        bot.send_message(m.chat.id, lang.start[conf_menu.lang], reply_markup=keyboard.main_menu())
    elif m.text == 'Bitmex':
        conf_menu.list_conf[0] = 'bitmex'
        bot.send_message(m.chat.id, m.text, reply_markup=keyboard.bitmex_symbol_menu())
        print(conf_menu.list_conf)
    elif m.text == "🔷BTC" \
            or m.text == "🔷EOS" \
            or m.text == "🔷XRP" \
            or m.text == "🔷TRX" \
            or m.text == "🔷ADA" \
            or m.text == "🔷BCH" \
            or m.text == "🔷LTC" \
            or m.text == "🔷ETH":
        if m.text == "🔷BTC":
            conf_menu.list_conf.append('XBT')
            print(conf_menu.list_conf)
            bot.send_message(m.chat.id, m.text, reply_markup=keyboard.coin_menu())
        else:
            conf_menu.list_conf.append(m.text[1:])
            bot.send_message(m.chat.id, m.text, reply_markup=keyboard.coin_menu())
    elif m.text == 'Bitfinex':
        conf_menu.list_conf[0] = 'bitfinex'
        bot.send_message(m.chat.id, m.text, reply_markup=keyboard.bitfinex_symbol_menu())
    elif m.text == '❇BTC' \
            or m.text == '❇ETH' \
            or m.text == '❇BSV' \
            or m.text == '❇XTZ' \
            or m.text == '❇LTC' \
            or m.text == '❇EOS':
        conf_menu.list_conf.append(m.text[1:])
        bot.send_message(m.chat.id, m.text, reply_markup=keyboard.coin_menu())
    elif m.text == "Binance":
        conf_menu.list_conf[0] = 'binance'
        bot.send_message(m.chat.id, m.text, reply_markup=keyboard.binance_symbol_menu())
    elif m.text == "🔶BTC" \
            or m.text == "🔶BNB" \
            or m.text == "🔶XRP" \
            or m.text == "🔶ETH" \
            or m.text == "🔶BCH" \
            or m.text == "🔶LTC":
        conf_menu.list_conf.append(m.text[1:])
        bot.send_message(m.chat.id, m.text, reply_markup=keyboard.coin_menu())
    elif m.text == 'Вернуться в начальное меню ⬅' or m.text == 'Return to the start menu ⬅':
        print(m.text == 'Return to the start menu ⬅')
        bot.send_message(m.chat.id, m.text, reply_markup=keyboard.main_menu())
        conf_menu.list_conf = [' ']
        conf_menu.date = []
    elif m.text == '📊 Статистика за период 📊' or m.text == '📊 Statistics for the period 📊':
        bot.send_message(m.chat.id, lang.en_dt[conf_menu.lang])
    elif m.text == '❇ Старт ❇' or m.text == '❇ Start ❇':
        if conf_menu.list_conf[0] == 'bitmex':
            start_bitmex(m, conf_menu.list_conf[1], conf_menu.list_conf[2],conf_menu.list_conf[3])
        if conf_menu.list_conf[0] == 'bitfinex':
            start_bitfinex(m, conf_menu.list_conf[1], conf_menu.list_conf[2],conf_menu.list_conf[3])
        if conf_menu.list_conf[0] == 'binance':
            start_binance(m, conf_menu.list_conf[1], conf_menu.list_conf[2],conf_menu.list_conf[3])
    elif m.text == '🛑 Стоп 🛑' or m.text == '🛑 Stop 🛑':
        global flag_stream
        flag_stream = False
        bot.send_message(m.chat.id, m.text, lang.start[conf_menu.lang], reply_markup=keyboard.main_menu())
        conf_menu.list_conf = [' ']
    elif m.text == '⚡ Стрим сделок ⚡' or m.text == '⚡ Stream deals ⚡':
        bot.send_message(m.chat.id, 'Введите интервал времени в минутах по примеру\n/l <min> <max>')
    else:
        bot.send_message(m.chat.id, lang.error[conf_menu.lang], reply_markup=keyboard.main_menu())
        conf_menu.list_conf = ['']


bot.polling(none_stop=True)
