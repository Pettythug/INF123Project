"""
Server master:
The server is almighty.
Every frame, it receives player inputs from clients,
executes these inputs to update the game state,
and sends the whole game state to all the clients for display.
"""
from __future__ import division # So to make division be float instead of int
from network import Server, RemoteClient
from random import randint
from time import sleep
import asyncore
import cPickle as pickle
from collections import OrderedDict
#dictionary key: event name
#   value = args to event function

##################### game logic #############
# game state
borders = [[0, 0, 2, 300], [0, 0, 400, 2], [398, 0, 2, 300], [0, 298, 400, 2]]
pellets = [[randint(10, 390), randint(10, 290), 5, 5] for _ in range(4)]
players = {}  # map a client handler to a player object

# map inputs received from clients to directions
input_dir = {'up': [0, -1], 'down': [0, 1],
             'left': [-1, 0], 'right': [1, 0]}

event_queue = []  # list of ('event', handler)
# 'event' can be 'quit', 'join', 'up', 'down', 'left', 'right'

class Player(RemoteClient):

    """A player object on the server."""

    def __init__(self, *args, **kwargs):
        RemoteClient.__init__(self, *args, **kwargs)

        # Preloaded event functions
        self.events = {'join': self.do_join,
                       'quit': self.do_quit,
                       'space': self.throw_snowball,
                       'update_players': self.update_players,
                       'move': self.do_move,
                       'spawn': self.do_spawn,
                       'input': self.do_change_dir}

        self.revive()

    def revive(self):
        self.box = [0, 0, 10, 10]
        self.input = 'down'
        self.change_dir(self.input)  # original direction: downwards
        self.speed = 5

    def change_dir(self, input):
        self.dir = input_dir[input]
        self.input = input

    def throw_snowball(self, sender_id, data):
        pass

    def update_players(self, sender_id, data):
        pass

    def do_spawn(self, sender_id, data):
        """
           Creates an enemy id and keeps track of the id on the server.
           This method is a precursor to actually spawning the enemy and will send
           the create_enemy event to all the connected clients.
        """

        enemy_id = self.server.generate_enemy_id()
        for remote_client in self.server.remote_clients:
            remote_client.do_send({'create_enemy': [enemy_id]+data}, remote_client.name)

    def move(self):
        self.box[0] += self.dir[0] * self.speed
        self.box[1] += self.dir[1] * self.speed

    def grow_and_slow(self, qty=2):
        self.box[2] += qty
        self.box[3] += qty
        self.speed -= self.speed/6

    def do_join(self, sender_id, data):
        self.friendly_name = data
        for remote_client in self.server.remote_clients:
            if remote_client.name != self.name:
                self.do_send({'join': remote_client.friendly_name}, remote_client.name)
                self.do_send({'move':[remote_client.box[0], remote_client.box[1]], 'input': remote_client.input}, remote_client.name)

    def do_quit(self, sender_id, data):
        pass

    def do_move(self, sender_id, data):
        # This isn't used right now because the update function below was too slow
        self.box[0] = data[0]
        self.box[1] = data[1]

    def do_change_dir(self, sender_id, data):
        self.change_dir(data)

    def on_open(self):
        #self.do_send({'join', self.name})
        pass

    def on_close(self):
        #self.do_send('quit', self.name)
        pass

    def on_msg(self, data):
        sender_id, data = data

        # Process events
        for event in self.events:
            if event in data:
                #Calls the function specified by the event
                self.events[event](sender_id, data[event])


def collide_boxes(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    return x1 < x2 + w2 and y1 < y2 + h2 and x2 < x1 + w1 and y2 < y1 + h1

################### network ##############

class GameServer(Server):

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.players = self.remote_clients
        self.next_enemy_id = 0

    def generate_enemy_id(self):
        self.next_enemy_id += 1
        return str(self.next_enemy_id)

    def poll(self):
        asyncore.loop(timeout=0, count=1) # return right away

    def serve(self):
        while True:
            self.poll()

            #I wasn't sure what to do with this section, because
            #it didn't really make sense to me.

            # move everyone and detect collisions
            for player in self.players:
                #player.move()
                for border in borders:  # collision with borders
                    if collide_boxes(player.box, border):
                        player.revive()
                for p in self.players:  # collision with other players
                     # only the player with lowest id of the pair detects the collision
                    if player.name < p.name and collide_boxes(player.box, p.box):
                        playerw, pw = player.box[2], p.box[2]  # widths
                        if playerw > pw:
                            player.grow_and_slow(pw)
                            p.revive()
                        elif playerw < pw:
                            p.grow_and_slow(playerw)
                            player.revive()
                        else:  # they have same width: kill both
                            p.revive()
                            player.revive()
                for index, pellet in enumerate(pellets):  # collision with pellets
                    if collide_boxes(player.box, pellet):
                        player.grow_and_slow()
                        pellets[index] = [randint(10, 390), randint(10, 290), 5, 5]

            # I commented this out because it is way too slow to update. See the bottom of client.py
            # file for how I update with events instead

            # Send to all players 1) the whole game state, and 2) their own name,
            # so each player can draw herself differently from the other players.
            #serialized_players = {p.name: p.box for p in self.players}
            #for player in self.players:
            #    msg = {'borders': borders,
            #           'pellets': pellets,
            #           'myname': player.name,
            #           'update_players': serialized_players,
            #           'input': player.input}
            #    player.do_send(msg, player.name)

            sleep(1. / 24)  # seconds

server = GameServer(address=('', 8888), handler=Player)
try:
    server.serve()
except:
    server.handle_close()
    asyncore.loop()
######################### loop #######################

