from network import Listener, Handler, poll
from time import sleep


handlers = {}  # map client handler to user name
class MyHandler(Handler):
    
    def on_open(self):
        print "open"
        
        
    def on_close(self):
        for username in handlers.iterkeys():
            if handlers[username] is self:
                handlers.pop(username)
                break
        print "close"
    
    def on_msg(self, msg):
        if 'join' in msg:
            handlers[msg['join']]=self
            msgtosend='Users: '
            for username in handlers.iterkeys():
                msgtosend+=username+","
            msgtosend=msgtosend[:-1]
            for user in handlers.itervalues():
                user.do_send(msgtosend)
        if 'speak' in msg:
            if msg['txt'] == 'quit':
                msgtosend=msg['speak'] +" has left the room. Users: "
                for username in handlers.iterkeys():
                    if username != msg['speak'] :
                        msgtosend+=username+","
                msgtosend=msgtosend[:-1]
                for user in handlers.itervalues():
                    if user is not self:
                        user.do_send(msgtosend)
            else:
                print msg
                for user in handlers.itervalues():
                    if user is not self:
                        user.do_send(msg['speak']+": "+msg['txt'])

class Serv(Listener):
    handlerClass = MyHandler
    def on_accept(self,h):
        pass


port = 8888
server = Serv(port)
try:
    while 1:
        poll()
        sleep(0.05)  # seconds
except KeyboardInterrupt:
    for user in handlers.values():
        user.do_close()
    print "closed all users"
    raise
