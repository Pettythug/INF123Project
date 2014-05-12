import socket
import pygame
import json
import threading

interesting_keys = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,
                    pygame.K_SPACE]

class Server(object):
    def __init__(self):
        self.clients = []
        self.images_sent = set()

    def new_frame(self):
        self.to_send = []

    def draw(self, rect, image):
        if id(image) not in self.images_sent:
            # Data for this image was not yet sent to clients.
            size = image.get_size()
            data = pygame.image.tostring(image, 'RGBA')
            message = ['load', id(image), data.encode('base64'), size]
            self.to_send.append(message)
            self.images_sent.add(id(image))
        self.to_send.append(['draw', [rect.x, rect.y], id(image)])

    def end_frame(self):
        self.to_send.append(['end'])
        for i, client in enumerate(self.clients):
            self._send_frame_to_client(i, client)

    def _send_frame_to_client(self, client_i, client):
        for msg in self.to_send:
            client.write(json.dumps(msg) + '\n')
            client.flush()

    def client_updater(self, i):
        while True:
            # Read keys status from client.
            keys = json.loads(self.clients[i].readline())
            self.pressed_keys[i] = keys

    def start(self):
        n_players = int(raw_input('Number of players: '))
        # initially, all keys are off
        self.pressed_keys = [ [0] * 400 for i in xrange(n_players) ]
        # listen on TCP/IP socket
        listen_socket = socket.socket()
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind(('localhost', 8888))
        listen_socket.listen(5)
        # Wait for all players to connect
        for i in xrange(n_players):
            sock, addr = listen_socket.accept()
            print '%d player connected' % (i + 1)
            file = sock.makefile('r+')
            self.clients.append(file)

        for i in xrange(n_players):
            thread = threading.Thread(target=self.client_updater,
                                      args=[i])
            thread.daemon = True
            thread.start()
