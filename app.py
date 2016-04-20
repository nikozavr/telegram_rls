from flask import Flask, request
import telepot
from pprint import pprint

PORT = 8443
HOST = "telbotrls.herokuapp.com"
TOKEN = "194721710:AAFQcKrb9w7sDxqGlEtb66L_2C8DQw7KcP4"

app = Flask(__name__)

try:
    from Queue import Queue
except ImportError:
    from queue import Queue

def handle(msg):
    pprint(msg)

bot = telepot.Bot(TOKEN)
update_queue = Queue()
bot.message_loop(handle, source=update_queue)
print('Listening ...')

@app.route('/')
def index():
    return "Ok!"

@app.route("/" + TOKEN, methods=['GET', 'POST'])
def bot():
    update_queue.put(request.data)  # dump data to queue
    return 'OK'

if __name__ == "__main__":
    bot.setWebhook(webhook_url='https://%s:%s/%s' % (HOST, PORT, TOKEN))
    app.run(host='0.0.0.0',
            port=PORT,
            debug=True)
