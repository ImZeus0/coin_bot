from telebot import types
import gen_calendar
import conf_menu
import lang


def lang_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Russian 🇷🇺"),types.KeyboardButton("English 🏴󠁧󠁢󠁥󠁮󠁧󠁿"))
    return keyboard

def main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Binance"))
    keyboard.add(types.KeyboardButton("Bitmex"))
    keyboard.add(types.KeyboardButton("Bitfinex"))
    keyboard.add(types.KeyboardButton(lang.сhange_lang[conf_menu.lang]))
    return keyboard


def coin_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(lang.coin_menu[conf_menu.lang][0]))
    keyboard.add(types.KeyboardButton(lang.coin_menu[conf_menu.lang][1]))
    keyboard.add(types.KeyboardButton(lang.back[conf_menu.lang]))
    return keyboard

def inline_year():
    years = gen_calendar.generate_year()
    keyboard = types.InlineKeyboardMarkup()
    for year in years:
        keyboard.add(types.InlineKeyboardButton(text=str(year),callback_data=str(year)))
    return keyboard


def inline_mon():
    keyboard = types.InlineKeyboardMarkup()
    mons = gen_calendar.generate_mon()
    btn = []
    for mon in mons.values():
        btn.append(types.InlineKeyboardButton(text=str(mon),callback_data=str(mon)))
    for a in range(0, 12, 3):
        print(a,a+1,a+2,a+3)
        keyboard.add(btn[a], btn[a + 1], btn[a + 2])
    return keyboard

def inline_day(year,mon):
    keyboard = types.InlineKeyboardMarkup()
    days = gen_calendar.generate_day(year,mon)
    btn = []
    for day in days:
        btn.append(types.InlineKeyboardButton(text=str(day),callback_data=str(day)))
    for a in range(len(days)):
        keyboard.add(btn[a])
    return keyboard

def interval_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(lang.intr_menu[conf_menu.lang][0]))
    keyboard.add(types.KeyboardButton(lang.intr_menu[conf_menu.lang][1]))
    keyboard.add(types.KeyboardButton(lang.intr_menu[conf_menu.lang][2]))
    keyboard.add(types.KeyboardButton(lang.back[conf_menu.lang]))
    return keyboard


def bitmex_symbol_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("🔷BTC"), types.KeyboardButton("🔷XRP"), types.KeyboardButton("🔷TRX"))
    keyboard.add(types.KeyboardButton("🔷ADA"), types.KeyboardButton("🔷BCH"), types.KeyboardButton("🔷LTC"))
    keyboard.add(types.KeyboardButton("🔷ETH"), types.KeyboardButton("🔷EOS"))
    keyboard.add(types.KeyboardButton(lang.back[conf_menu.lang]))
    return keyboard


def binance_symbol_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("🔶BTC"), types.KeyboardButton("🔶BNB"), types.KeyboardButton("🔶XRP"))
    keyboard.add(types.KeyboardButton("🔶ETH"), types.KeyboardButton("🔶BCH"), types.KeyboardButton("🔶LTC"))
    keyboard.add(types.KeyboardButton(lang.back[conf_menu.lang]))
    return keyboard


def bitfinex_symbol_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("❇BTC"), types.KeyboardButton("❇ETH"), types.KeyboardButton("❇BSV"))
    keyboard.add(types.KeyboardButton("❇XTZ"), types.KeyboardButton("❇LTC"), types.KeyboardButton("❇EOS"))
    keyboard.add(types.KeyboardButton(lang.back[conf_menu.lang]))
    return keyboard

def stream_menu_1():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(lang.start_s[conf_menu.lang]))
    keyboard.add(types.KeyboardButton(lang.back[conf_menu.lang]))
    return keyboard


def stream_menu_2():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(lang.stop_s[conf_menu.lang]))
    return keyboard

def null():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    return keyboard

# def duo_menu():
