import socket, json, threading, logging
from pymongo import MongoClient
from os import chdir, path 


chdir(path.dirname(path.abspath(__file__)))
logging.basicConfig(
    filename = 'postmongo_socket.log',
    encoding = 'utf-8',
    format = '%(levelname)s @ %(asctime)s # %(message)s',
    level = logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

database = MongoClient("mongodb://host.docker.internal:27017").db1
RUNNING = True
dblock = threading.Lock()
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(('0.0.0.0',5050))
sock.settimeout(2)
sock.listen(5)
BUFFER_MAX = 1024
data_count = 0

def handler(c,counter):
    print('Handler')
    logging.info('handler')
    global RUNNING, data_count
    data = b''
    while True:
        recv = c.recv(BUFFER_MAX)
        data += recv
        if data[-3:] == b':::': break
    payload = json.loads(data.decode('utf-8')[:-3])
    if 'table' not in payload:
        RUNNING = False
        return
    collection_name = payload['table'].lower()
    data = payload['data']
    print(len(data))
    logging.info(len(data))
    with dblock:
        data_count += len(data)
        print(data_count)
        collection = database[collection_name]
        collection.insert_many(data)
    return

counter = 0
print("Started")
logging.info('started')
while RUNNING:
    try:
        try:
            c, addr = sock.accept() 
            print(addr)  
            counter += 1
            threading.Thread(target=handler, args=(c,counter)).start()
        except socket.error:
            pass
    except KeyboardInterrupt:
        break