#! /usr/bin/env python
# -*- coding: utf-8 -*-
from telebot import types
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

