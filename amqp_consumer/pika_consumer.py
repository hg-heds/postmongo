import functools
import logging
import threading
import json
import pika
from pika.exchange_type import ExchangeType
from pymongo import MongoClient
from os import chdir,path
chdir(path.dirname(path.abspath(__file__)))

logging.basicConfig(
    filename = 'postmongo_amqp.log',
    encoding = 'utf-8',
    format = '%(levelname)s @ %(asctime)s.%(msecs)03d # %(message)s',
    level = 21,
    datefmt='%Y-%m-%d %H:%M:%S'
)


database = MongoClient("mongodb://host.docker.internal:27017").db1
dblock = threading.Lock()


def ack_message(ch, delivery_tag):

    if ch.is_open:
        ch.basic_ack(delivery_tag)
    else:
        pass


def do_work(ch, delivery_tag, body):
    cb = functools.partial(ack_message, ch, delivery_tag)
    ch.connection.add_callback_threadsafe(cb)
    payload = json.loads(body.decode('utf-8'))
    collection_name = payload['table'].lower()
    data = payload['data']
    logging.log(21,len(data))
    with dblock:
        collection = database[collection_name]
        collection.insert_many(data)
    logging.log(22,len(data))


def on_message(ch, method_frame, _header_frame, body, args):
    thrds = args
    delivery_tag = method_frame.delivery_tag
    t = threading.Thread(target=do_work, args=(ch, delivery_tag, body))
    t.start()
    thrds.append(t)


credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters(
    'host.docker.internal', credentials=credentials, heartbeat=5)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()
channel.exchange_declare(
    exchange="test_exchange",
    exchange_type=ExchangeType.direct,
    passive=False,
    durable=True,
    auto_delete=False)
channel.queue_declare(queue="standard", auto_delete=True)
channel.queue_bind(
    queue="standard", 
    exchange="test_exchange", 
    routing_key="standard_key")
channel.basic_qos(prefetch_count=1)

threads = []
on_message_callback = functools.partial(on_message, 
                                        args=(threads))
channel.basic_consume(on_message_callback=on_message_callback, 
                      queue='standard')

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

# Wait for all to complete
for thread in threads:
    thread.join()

connection.close()