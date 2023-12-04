import psycopg2, socket, json
import psycopg2.extras
connection = psycopg2.connect(database='postgres', host='127.0.0.1', user='postgres', password='hughes@422', port='5432')
cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
cursor.execute('select * from "METODO"')
while True:
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect(('127.0.0.1',5050))
    res = cursor.fetchmany(10000)
    if not res: 
        sock.close()
        break
    sock.send(json.dumps({'table':'METODO','data':[dict(row) for row in res]}).encode('utf-8')+b':::')
    sock.close()
    
cursor.close()
connection.close()