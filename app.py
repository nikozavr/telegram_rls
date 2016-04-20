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



@app.route('/')
def index():
    return "Ok!"

@app.route("/bot", methods=['GET', 'POST'])
def bot():
    update_queue.put(request.data)  # dump data to queue
    return 'OK'

if __name__ == "__main__":
    app.run()
