import pika, psycopg2, json
from pika import DeliveryMode
from pika.exchange_type import ExchangeType

import psycopg2.extras
postgres = psycopg2.connect(database='postgres', host='127.0.0.1', user='postgres', password='hughes@422', port='5432')
cursor = postgres.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
cursor.execute('select * from "METODO"')


credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('localhost', credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.exchange_declare(exchange="test_exchange",
                         exchange_type=ExchangeType.direct,
                         passive=False,
                         durable=True,
                         auto_delete=False)


print("Sending message to create a queue")


connection.sleep(5)

while True:
    res = cursor.fetchmany(1000)
    if not res: break
    channel.basic_publish('test_exchange', 'standard_key', json.dumps({'table':'METODO','data':[dict(row) for row in res]}), pika.BasicProperties(content_type='text/plain', delivery_mode=DeliveryMode.Transient))

connection.close()
cursor.close()
postgres.close()