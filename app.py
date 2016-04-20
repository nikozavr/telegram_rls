from flask import Flask, request
import telepot
import pprint

app = Flask(__name__)

try:
    from Queue import Queue
except ImportError:
    from queue import Queue

def handle(msg):
    pprint(msg)

bot = telepot.Bot("194721710:AAFQcKrb9w7sDxqGlEtb66L_2C8DQw7KcP4")
update_queue = Queue()
bot.message_loop(handle, source=update_queue)
print('Listening ...')

@app.route('/')
def index():
    return "Ok!"

@app.route("/bot", methods=['GET', 'POST'])
def bot():
    update_queue.put(request.data)  # dump data to queue
    return 'OK'

if __name__ == "__main__":
    bot.setWebhook("https://telbotrls.herokuapp.com/bot")
    app.run()
