import socket, json, threading, logging
from pymongo import MongoClient
from os import chdir,path 
chdir(path.dirname(path.abspath(__file__)))
logging.basicConfig(
    filename = 'postmongo_socket.log',
    encoding = 'utf-8',
    format = '%(levelname)s @ %(asctime)s.%(msecs)03d # %(message)s',
    level = 21,
    datefmt='%Y-%m-%d %H:%M:%S'
)

database = MongoClient("mongodb://localhost:27017").db1
dblock = threading.Lock()
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(('127.0.0.1',5050))
sock.settimeout(2)
sock.listen(5)
BUFFER_MAX = 1024

def handler(c):
    data = b''
    while True:
        recv = c.recv(BUFFER_MAX)
        data += recv
        if data.endswith(b':::'): break
    payload = json.loads(data.decode('utf-8')[:-3])
    collection_name = payload['table'].lower()
    data = payload['data']
    logging.log(21,len(data))
    with dblock:
        collection = database[collection_name]
        collection.insert_many(data)
    logging.log(22,len(data))

while True:

    try:
        c, addr = sock.accept() 
        threading.Thread(target=handler, args=(c,)).start()
    except socket.error:
        pass
