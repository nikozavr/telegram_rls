import sys
import time
import pprint
import telepot
import requests
import urllib
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup

num = 0
gettingnum = False
links = []


def parse_resp(response, msg):
    global gettingnum
    if response.getcode() == 200:
        the_page = response.read().decode('cp1251')
        soup = BeautifulSoup(the_page, 'html.parser')
        dv = False
        answer = "*" + msg["text"][3:] + "*" + "\n"
        if soup.find(id="page_head").string != None:
            div = soup.find(id="content")
            if div.find("div", { "class" : "search_serp_one" }) != None:
                answer = answer + "Выберите вариант, введя его номер\n"
                answer = answer + " Варианты:\n"
                count = 0
                global links
                links = []
                for div in soup.find_all("div", { "class" : "search_serp_one" }):
                    count = count + 1
                    links.append(div.find_all('a')[0]['href'])
                    print(links)
                    answer = answer + "  " + str(count) + " " + (div.find_all('a')[0]).getText() + "\n"
                    if div.next_sibling.name == "p":
                        break
                gettingnum = True
            else:
                bot.sendMessage(msg['chat']['id'], 'Ошибка поиска. Проверьте название препарата')
                return

        else:
            for item in soup.find_all('a'):
                if item.has_attr('href'):
                    if item['href'] == "#d-izobrazheniya":
                        dv = False
                        answer = answer + "\n"
                elif item.has_attr('name'):
                    if item['name'] == "atx":
                        dv = False
                        answer = answer + "\n"

                if dv:
                    answer = answer + "  -" + item.string + "\n"

                if item.has_attr('name'):
                    if item['name'] == "dejstvuyushhee-veshhestvo":
                        answer = answer + " Дествующее вещество:\n"
                        dv = True
                print(item)


        bot.sendMessage(msg['chat']['id'], answer, parse_mode="Markdown" )
    else:
        bot.sendMessage(msg['chat']['id'], 'Ошибка поиска. Проверьте название препарата')


def handle(msg):
    print(msg)
    pprint.pprint(msg)
    global gettingnum
    if not gettingnum:
        if len(msg['text']) > 2:
            if msg['text'][:2] == "/s":
                values = {'word' : msg["text"][3:],
                            'encoding' : "utf-8"}
                url = "http://www.rlsnet.ru/search.htm"
                data = urllib.parse.urlencode(values)
                data = data.encode('utf-8') # data should be bytes
                req = urllib.request.Request(url, data)
                response = urllib.request.urlopen(req)
                parse_resp(response, msg)

            elif msg['text'][:2] == "/h":
                bot.sendMessage(msg['chat']['id'], 'Бот предназначен для поиска лекарств на сайте http://www.rlsnet.ru/')
            else:
                bot.sendMessage(msg['chat']['id'], 'Для поиска введите /s и точное название препарата')
        else:
            bot.sendMessage(msg['chat']['id'], 'Для поиска введите /s и точное название препарата')
    else:
        try:
            global links
            num = int(msg['text'])
            gettingnum = False
            if num > 0:
                url = links[num]
                req = urllib.request.Request(url)
                response = urllib.request.urlopen(req)
                parse_resp(response, msg)
                links=[]
            else:
                bot.sendMessage(msg['chat']['id'], 'Ошибка ввода')
        except ValueError:
            bot.sendMessage(msg['chat']['id'], 'Ошибка ввода')


bot = telepot.Bot("194721710:AAFQcKrb9w7sDxqGlEtb66L_2C8DQw7KcP4")

bot.message_loop(handle)
print('Listening ...')

while 1:
    time.sleep(10)
