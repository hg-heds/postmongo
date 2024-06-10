import psycopg2, socket, json
import psycopg2.extras, logging
from os import chdir, path 
chdir(path.dirname(path.abspath(__file__)))
logging.basicConfig(
    filename = 'postmongo_socket.log',
    encoding = 'utf-8',
    format = '%(levelname)s @ %(asctime)s # %(message)s',
    level = logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
logging.info("started")
connection = psycopg2.connect(database='postgres', host='host.docker.internal', user='postgres', password='SENHA', port='5432')
cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
cursor.execute('select * from "METODO"')
while True:
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect(('host.docker.internal',5050))
    res = cursor.fetchmany(1000)
    logging.info(len(res))
    if not res: 
        sock.close()
        break
    sock.send(json.dumps({'table':'METODO','data':[dict(row) for row in res]}).encode('utf-8')+b':::')
    sock.close()
    
cursor.close()
connection.close()