import logging
from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from numpy import random
from wsgiref.simple_server import make_server

strings = ["Lorem ipsum dolor sit amet, ",
"consectetur adipiscing elit, ",
"sed do eiusmod tempor ",
"incididunt ut labore et dolore ",
"magna aliqua. Ut enim ad minim ",
"veniam, quis nostrud ",
"exercitation ullamco laboris ",
"nisi ut aliquip ex ea commodo ",
"consequat. Duis aute irure ",
"dolor in reprehenderit in ",
"voluptate velit esse cillum ",
"dolore eu fugiat nulla ",
"pariatur. Excepteur sint ",
"occaecat cupidatat non ",
"proident, sunt in culpa qui",
"officia deserunt mollit anim",
"id est laborum"]

class HelloWorldService(ServiceBase):
    @rpc(Integer, _returns=Iterable(Unicode))
    def say_hello(ctx, times):
        for _ in range(times):
            yield strings[random.randint(len(strings))]

application = Application([HelloWorldService], 'spyne.examples.hello.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11(polymorphic=True))

wsgi_application = WsgiApplication(application)


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    logging.info("listening to http://127.0.0.1:8008")
    logging.info("wsdl is at: http://localhost:8008/?wsdl")

    server = make_server('127.0.0.1', 8008, wsgi_application)
    server.serve_forever()