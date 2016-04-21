from flask import Flask, request
import telepot
from pprint import pprint
import sys
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from httplib2 import Http

PORT = 443
HOST = "telbotrls.herokuapp.com"
TOKEN = "194721710:AAFQcKrb9w7sDxqGlEtb66L_2C8DQw7KcP4"

app = Flask(__name__)

num = 0
gettingnum = False
links = []

try:
    from Queue import Queue
except ImportError:
    from queue import Queue

def parse_resp(resp, content, msg):
    global gettingnum
    if resp.status == 200:
        the_page = content.decode("cp1251", "ignore")
        print(the_page)
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
    pprint(msg)
    global gettingnum
    if not gettingnum:
        if len(msg['text']) > 2:
            if msg['text'][:2] == "/s":
                values = {'word' : msg["text"][3:],
                            'encoding' : "utf-8"}
                url = "http://www.rlsnet.ru/search.htm"
                data = urlencode(values)
                data = data.encode('utf-8')

                h = Http()
                resp, content = h.request(url, "GET", data)
                print(resp.status)
                print(content)
                parse_resp(resp, content, msg)

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

bot = telepot.Bot(TOKEN)
update_queue = Queue()
bot.message_loop(handle, source=update_queue)
print('Listening ...')

@app.route('/')
def index():
    return "Ok!"

@app.route("/" + TOKEN, methods=['GET', 'POST'])
def webhook():
    update_queue.put(request.data)  # dump data to queue
    return 'OK'

if __name__ == "__main__":
    bot.setWebhook(webhook_url='https://%s:%s/%s' % (HOST, PORT, TOKEN))
    app.run(host='0.0.0.0',
            port=PORT,
            debug=True)
