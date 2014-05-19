"""
Simple JSON wrapper on top of asyncore TCP sockets.
Provides on_open, on_close, on_msg, do_send, and do_close callbacks.

Public domain

With inspiration from:
http://pymotw.com/2/asynchat/
http://code.google.com/p/podsixnet/
http://docstore.mik.ua/orelly/other/python/0596001886_pythonian-chp-19-sect-3.html


#################
# Echo server:
#################
from network import Listener, Handler, poll

class MyHandler(Handler):
    def on_msg(self, data):
        self.do_send(data)

class EchoServer(Listener):
    handlerClass = MyHandler

server = EchoServer(8888)
while 1:
    poll()


#################
# One-message client:
#################
from network import Handler, poll

done = False

class Client(Handler):
    def on_open(self):
        self.do_send({'a': [1,2], 5: 'hi'})
        global done
        done = True

client = Client('localhost', 8888)
while not done:
    poll()
client.do_close()

"""

from __future__ import print_function

import asyncore
import collections
import logging
import socket
import json

#Uncomment this to see logging info
#logging.basicConfig(level=logging.INFO)

MAX_MESSAGE_LENGTH=2048

# This will keep from messages building up. Increase for smoother appearance, but slower performance
# and decrease for a little more studder but faster performance. Also,
# this should be greater than or equal to the number of players desired
MAX_QUEUE_SIZE = 8

class Client(asyncore.dispatcher):

    """ Represents a local client. This is used to keep track of the local player."""

    def __init__(self, host, port, name):
        asyncore.dispatcher.__init__(self)

        # Sets the logger for this class. The self.__class__.__name__ is just so that
        # if we change the name of the class, we don't have to update this piece of code
        self.log = logging.getLogger('{class_name} ({client_name})'.format(class_name=self.__class__.__name__,
                                                                           client_name=name))
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = name
        self.log.info('Connecting to host at {}'.format((host, port)))
        self.connect((host, port))
        # a dequeue is faster than an array
        self.outbox = collections.deque()
        self.terminator = '\n'

    def do_send(self, message):
        encoded_message = json.dumps(message, -1)        
        if len(self.outbox) > MAX_QUEUE_SIZE:  #makes sure queue is a certain size
            self.outbox.popleft()
        self.outbox.append(encoded_message)
        self.log.info('Enqueued message: {}'.format(message))

    def handle_write(self):
        if not self.outbox:
            return
        message = self.outbox.popleft()+self.terminator
        if len(message) > MAX_MESSAGE_LENGTH:
            raise ValueError('Message too long')
        self.send(message) #send message to socket

    def handle_read(self):
        # split the messages in case we get multiple at once
        # the -1 is to remove the last element in the list
        messages = self.recv(MAX_MESSAGE_LENGTH).split(self.terminator)[:-1]
        for m in messages:
                message = json.loads(m)
                self.log.info('Received message: {}'.format(message))
                self.on_msg(message)

    def handle_close(self):
        self.close()
        self.on_close()

    def do_close(self):
        self.handle_close()

    def handle_connect(self):
        self.on_open()

    def on_msg(self, data):
        pass

    def on_open(self):
        pass

    def on_close(self):
        pass

#asyncore
class RemoteClient(asyncore.dispatcher):

    """Wraps a remote client socket."""

    def __init__(self, server, host, port, sock=None, name=''):
        if sock:  # passive side: Handler automatically created by a Listener
            asyncore.dispatcher.__init__(self, sock)
        else:  # active side: Handler created manually
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
            asyncore.dispatcher.__init__(self, sock)
            self.connect((host, port))  # asynchronous and non-blocking

        self.name = name
        self.friendly_name = self.name
        self.server = server
        self.outbox = collections.deque()
        self.terminator = '\n'

    def do_send(self, message, sender_id):
        message = json.dumps((sender_id, message), -1)
        if len(self.outbox) > MAX_QUEUE_SIZE:
            self.outbox.popleft()
        self.outbox.append(message)

    #when a message is read from the outbox
    #self.outbox = collections.deque()
    def handle_read(self):
        try:
            # split the messages in case we get multiple at once
            # the -1 is to remove the last element in the list
            client_message = self.recv(MAX_MESSAGE_LENGTH)
            messages = client_message.split(self.terminator)[:-1] #too many messages at the same time. Splits messages to parse
            for m in messages:
                self.server.broadcast(m, self.name)
                self.on_msg((self.name, json.loads(m)))
        except EOFError: #If we disconnect unexpectedly
            self.server.log.info('Client {} Disconnected.'.format(self.friendly_name))
            self.handle_close()

    def handle_close(self):
        self.close()
        self.on_close()
        if self in self.server.remote_clients:
            self.server.remote_clients.remove(self)

    def do_close(self):
        self.handle_close()

    def handle_connect(self):
        self.on_open()

    def handle_write(self):
        if not self.outbox:
            return
        message = self.outbox.popleft()+self.terminator
        if len(message) > MAX_MESSAGE_LENGTH:
            raise ValueError('Message too long')
        self.send(message)

    def on_msg(self, data):
        pass

    def on_open(self):
        pass

    def on_close(self):
        pass

#asyncore.dispatcher - generic class to send and receive messages between other 
#of the same classes

class Server(asyncore.dispatcher):

    def __init__(self, address=('localhost', 8888), handler=None):
        asyncore.dispatcher.__init__(self)
        self.next_player_id = 0

        self.handler = handler or RemoteClient
        #The name of the current class for the logger
        self.log = logging.getLogger(self.__class__.__name__)

        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(address)
        self.listen(5)
        self.remote_clients = []
        self.terminator = '\n'

        #make an id for a newly connected player
    def generate_name(self):
        self.next_player_id += 1
        return str(self.next_player_id)

    def handle_accept(self):
        socket, (host, port) = self.accept() # For the remote client.
        self.log.info('Accepted client at {}'.format((host, port)))
        h = self.handler(self, host, port, socket, name=self.generate_name())
        self.remote_clients.append(h)
        self.on_accept(h)
        h.on_open()

    def handle_read(self):
        message = json.loads(self.read())
        self.log.info('Received message: {}'.format(message))

    def broadcast(self, message, client_id):
        try:
            message = json.loads(message)
            self.log.info('Broadcasting message: {}'.format(message))
            for remote_client in self.remote_clients:
                remote_client.do_send(message, client_id)
        except EOFError: #If the client disconnects unexpectedly
            self.log.info('Client {} closed.'.format(client_id))

    def handle_close(self):
        for rc in self.remote_clients:
            rc.handle_close()
        self.close()

    def stop(self):
        self.handle_close()

    def on_accept(self, handler):
        pass

    def serve(self):
        asyncore.loop()

def poll():
    asyncore.loop(timeout=0, count=1)
