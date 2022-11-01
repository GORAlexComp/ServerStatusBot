# -*- coding: utf-8 -*-
'''
Author : GORAlex Comp
Date : 01/11/2022
'''

import os
import re
import telebot
import configparser
from dotenv import load_dotenv

config = configparser.ConfigParser()  # make parser object
config.read("config.cfg")  # read config

# load API_KEY from .env
# put your API_KEY in ".env" file
# API_KEY=<token>
load_dotenv()
API_KEY = os.getenv("API_KEY")

# make a connection to bot
bot = telebot.TeleBot(API_KEY)

# start and help command
@bot.message_handler(commands=['start','help'])
def help(message):
    msg = '''
*Бот мониторинга Dolphin для _TrafficAngels_*
\-\-\-\-\-\-\-\-\-
_*1\.*_ Использование дисков → /disk
_*2\.*_ Использование CPU и RAM → /sysinfo
_*3\.*_ Задержка сервера → /uptime
_*4\.*_ Описание сервера → /server
_*5\.*_ Помощь → /help
_*6\.*_ О боте → /about'''
    bot.send_message(message.chat.id, msg, parse_mode='MarkdownV2')

# make command function to chat if command receive
@bot.message_handler(commands=['check'])
def check(message):
    bot.send_message(message.chat.id, "*Бот доступен*", parse_mode='MarkdownV2')

# get system info
import psutil
import subprocess

# disk usage (/disk)
@bot.message_handler(commands=['disk'])
def disk(message):
    diskTotal = re.escape(str(round(psutil.disk_usage('/').total/(1024*1024*1024),3)))
    diskUsed = re.escape(str(round(psutil.disk_usage('/').used/(1024*1024*1024),3)))
    diskAvail = re.escape(str(round(psutil.disk_usage('/').free/(1024*1024*1024),3)))
    diskPercent = re.escape(str(round(psutil.disk_usage('/').percent,3)))

    msg = '''
*Использование дисков*
\-\-\-\-\-\-\-\-\-
_*Всего*_ \= {} GB
_*Используется*_ \= {} GB  \({} %\)
_*Доступно*_ \= {} GB'''.format(diskTotal,diskUsed,diskPercent,diskAvail)
    bot.send_message(message.chat.id,msg, parse_mode='MarkdownV2')

# cpu & ram (/sysinfo)
@bot.message_handler(commands=['sysinfo'])
def sysinfo(message):
    cpuUsage = re.escape(str(psutil.cpu_percent(interval=1)))
    ramTotal = re.escape(str(int(psutil.virtual_memory().total/(1024*1024))))
    ramUsage = re.escape(str(int(psutil.virtual_memory().used/(1024*1024))))
    ramFree = re.escape(str(int(psutil.virtual_memory().free/(1024*1024))))
    ramUsagePercent = re.escape(str(psutil.virtual_memory().percent))
    msg = '''
*Использование CPU и RAM*
\-\-\-\-\-\-\-\-\-
_*Использование CPU*_ \= {} %

__Оперативная память__
_*Всего*_ \= {} MB
_*Используется*_ \= {} MB \({} %\)
_*Доступно*_  \= {} MB'''.format(cpuUsage,ramTotal,ramUsage,ramUsagePercent,ramFree)
    bot.send_message(message.chat.id,msg, parse_mode='MarkdownV2')

# uptime (/uptime)
@bot.message_handler(commands=['uptime'])
def uptime(message):
    upTime = subprocess.check_output(['uptime','-p']).decode('UTF-8')
    msg = upTime
    bot.send_message(message.chat.id,msg, parse_mode='MarkdownV2')

# server desc (/server)
@bot.message_handler(commands=['server'])
def server(message):
    uname = re.escape(str(subprocess.check_output(['uname','-rsoi']).decode('UTF-8')))
    host = re.escape(str(subprocess.check_output(['hostname']).decode('UTF-8')))
    ipAddr = re.escape(str(subprocess.check_output(['hostname','-I']).decode('UTF-8')))
    msg ='''
*Описание сервера*
\-\-\-\-\-\-\-\-\-
_*Операционная система*_ \= {}
_*Имя системы*_ \= {} 
_*IP адрес*_ \= {}'''.format(uname,host,ipAddr)
    bot.send_message(message.chat.id,msg, parse_mode='MarkdownV2')

# server desc (/about)
@bot.message_handler(commands=['about'])
def server(message):
    author = re.escape(str(config['main']['author']))
    version = re.escape(str(config['main']['version']))
    source = re.escape(str(config['main']['source']))
    commands = config['main']['commands']
    msg ='''
*О боте*
\-\-\-\-\-\-\-\-\-
Автор: @{}
Версия бота: {}
Исходный код: {}
Количество команд: {}'''.format(author,version,source,commands)
    bot.send_message(message.chat.id,msg, parse_mode='MarkdownV2', disable_web_page_preview=True)

# listen to telegram commands
bot.polling()
