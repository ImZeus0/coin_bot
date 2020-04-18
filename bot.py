import telebot
import config
import keyboard
import parse
import time
import binance_pars
import bitmex_pars
import os
import gen_calendar
import conf_menu
import lang

language = 0
flag_stream = True

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Выберете язык / Choose a language', reply_markup=keyboard.lang_menu())


@bot.message_handler(commands=['i'])
def any_msg(message):
    bot.send_message(message.chat.id, "select year", reply_markup=keyboard.inline_year())


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    years = gen_calendar.generate_year()
    mons = gen_calendar.generate_mon()
    if call.message:
        for year in years:
            if call.data == str(year):
                # conf_menu.date[0]year
                # bot.send_message(call.message.chat.id,call.data)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="chose mon", reply_markup=keyboard.inline_mon())
        for mon in mons.values():
            if call.data == str(mon):
                conf_menu.date.append(mon)
                # bot.send_message(call.message.chat.id,call.data)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="chose day",
                                      reply_markup=keyboard.inline_day(conf_menu.date[0], conf_menu.date[1]))
        days = gen_calendar.generate_day(conf_menu.date[0], conf_menu.date[1])
        for day in days:
            if call.data == str(day):
                conf_menu.date.append(day)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=str(day))
    print(conf_menu.date)


def reply_binanse_statistic(a):
    return str(a[0]) + '\n\n' + a[7] + lang.stat_text[conf_menu.lang][0] + str(a[1]) + lang.stat_text[conf_menu.lang][
        2] + str(a[2]) + lang.stat_text[conf_menu.lang][3] + str(
        a[3]) + lang.stat_text[conf_menu.lang][1] + str(a[4]) + lang.stat_text[conf_menu.lang][4] + str(a[5]) + \
           lang.stat_text[conf_menu.lang][5] + str(a[6])


def reply_bitfinex_statistic(a):
    return str(a[0]) + '\n\n' + a[6] + lang.stat_text[conf_menu.lang][0] + str(a[1]) + lang.stat_text[conf_menu.lang][
        2] + str(a[2]) + lang.stat_text[conf_menu.lang][3] + str(
        a[3]) + lang.stat_text[conf_menu.lang][1] + str(a[4]) + lang.stat_text[conf_menu.lang][4] + str(a[5])


def start_bitmex(m, symbol, min):
    global flag_stream
    flag_stream = True
    bot.send_message(m.chat.id, 'Start striming', reply_markup=keyboard.stream_menu_2())
    while flag_stream:
        reply = bitmex_pars.get_trades(symbol, min, 0)
        print(reply)
        if reply != 'none':
            bot.send_message(m.chat.id, reply)
        time.sleep(1)


def start_binance(m, symbol, min):
    global flag_stream
    flag_stream = True
    bot.send_message(m.chat.id, 'Start striming', reply_markup=keyboard.stream_menu_2())
    while flag_stream:
        reply = binance_pars.get_trades(symbol, min)
        print(reply)
        if reply != 'none':
            bot.send_message(m.chat.id, reply)
        time.sleep(1)


def start_bitfinex(m, symbol, min):
    global flag_stream
    flag_stream = True
    bot.send_message(m.chat.id, 'Start striming', reply_markup=keyboard.stream_menu_2())
    while flag_stream:
        reply = parse.get_trades(symbol, min, 0)
        print(reply)
        if reply != 'none':
            bot.send_message(m.chat.id, reply)
        time.sleep(3)


@bot.message_handler(commands=['m'])
def date(m):
    msg = m.text.split(' ')
    conf_menu.list_conf.append(int(msg[1]))
    bot.send_message(m.chat.id, lang.en_amm[conf_menu.lang])


@bot.message_handler(commands=['limit'])
def limit(m):
    mim = m.text.split(' ')
    if len(conf_menu.list_conf) == 2 and len(mim) == 2:
        conf_menu.list_conf.append(float(mim[1]))
        bot.send_message(m.chat.id, 'Press start', reply_markup=keyboard.stream_menu_1())
    elif len(conf_menu.list_conf) == 3:
        conf_menu.list_conf.append(float(mim[1]))
        print(conf_menu.list_conf[2])
        print(conf_menu.list_conf[3])
        if conf_menu.list_conf[0] == 'binance':
            msg = binance_pars.repry_statistic(
                binance_pars.trade_for_period(conf_menu.list_conf[1], conf_menu.list_conf[2], conf_menu.list_conf[3]))
            if len(msg) < 4000:
                bot.send_message(m.chat.id, msg,reply_markup=keyboard.main_menu())
                conf_menu.list_conf = [' ']
            else:
                with open('statistic.txt', 'w') as l:
                    l.write(msg)
                with open('statistic.txt', 'rb') as r:
                    red = r.read()
                bot.send_document(m.chat.id, red,reply_markup=keyboard.main_menu())
                conf_menu.list_conf = [' ']
                os.remove('statistic.txt')

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
            start_bitmex(m, conf_menu.list_conf[1], float(conf_menu.list_conf[2]))
        if conf_menu.list_conf[0] == 'bitfinex':
            start_bitfinex(m, conf_menu.list_conf[1], float(conf_menu.list_conf[2]))
        if conf_menu.list_conf[0] == 'binance':
            start_binance(m, conf_menu.list_conf[1], float(conf_menu.list_conf[2]))
    elif m.text == '🛑 Стоп 🛑' or m.text == '🛑 Stop 🛑':
        global flag_stream
        flag_stream = False
        bot.send_message(m.chat.id, m.text, lang.start[conf_menu.lang], reply_markup=keyboard.main_menu())
        conf_menu.list_conf = [' ']
    elif m.text == '⚡ Стрим сделок ⚡' or m.text == '⚡ Stream deals ⚡':
        bot.send_message(m.chat.id, lang.en_amm[conf_menu.lang], reply_markup=keyboard.null())
    else:
        bot.send_message(m.chat.id, lang.error[conf_menu.lang], reply_markup=keyboard.main_menu())
        conf_menu.list_conf = ['']


bot.polling(none_stop=True)
