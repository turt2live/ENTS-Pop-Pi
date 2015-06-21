import gevent
from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin
import threading

class PopNamespace(BaseNamespace, BroadcastMixin):
    def recv_connect(self):
        print "socket.io agent connected"

class Application(object):
    def __init__(self):
        self.buffer = []

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO'].strip('/') or 'index.html'

        if path.startswith('static/') or path == 'index.html':
            try:
                data = open('../www/' + path).read()
            except Exception:
                return not_found(start_response)

            if path.endswith(".js"):
                content_type = "text/javascript"
            elif path.endswith(".css"):
                content_type = "text/css"
            elif path.endswith(".png"):
                content_type = "image/png"
            else:
                content_type = "text/html"

            start_response('200 OK', [('Content-Type', content_type)])
            return [data]

        if path.startswith("socket.io"):
            socketio_manage(environ, {'/pop': PopNamespace})
        else:
            return not_found(start_response)


def not_found(start_response):
    start_response('404 Not Found', [])
    return ['<h1>Not Found</h1>']

class WebService:
    def __init__(self, bindAddress, port):
        print("Web server starting on {bindAddress}:{port} ...");
        self.__port = port
        self.__bindAddr = bindAddress
        self.webThread = threading.Thread(target=self.__start)
        self.webThread.daemon = True
        self.webThread.start()

    def __start(self):
        self.server = SocketIOServer((self.__bindAddr, self.__port), Application())
        gevent.spawn(self.__onStart)
        self.server.serve_forever()

    def __onStart(self):
        print "Web server started on {self.__bindAddr}:{self.__port} "

    def __broadcast(self, eventName, *args):
        pkt = dict(type="event",
                   name=eventName,
                   args=args,
                   endpoint="/pop")
        for sessid, socket in self.server.sockets.iteritems():
            socket.send_packet(pkt)

    # TODO: These "on" methods should be handled by Observer...
    def onSwipe(self, credit, cost):
        self.__broadcast("member-swipe", credit, cost)

    def onDeposit(self, cents):
        self.__broadcast("deposit", cents)

    def onPaid(self, newCredit):
        self.__broadcast("paid", newCredit)

    def onNotFound(self):
        self.__broadcast("not-found")

    def shutdown(self):
        return # Nothing to do
