import pygame
import socket
import sys
import json
from network import interesting_keys

SCREENWIDTH, SCREENHEIGHT = 640, 322

if sys.argv[1:]:
    host = sys.argv[1]
else:
    sys.exit('Usage: python client.py [server hostname]')

sock = socket.socket()
sock.connect((host, 8888))
sock_file = sock.makefile('r+', 1)

screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

images = {}

for line in sock_file:
    args = json.loads(line)
    if args[0] == 'load':
        # Load image to local cache.
        _, img_id, data, size = args
        image = pygame.image.fromstring(data.decode('base64'), tuple(size), 'RGBA')
        images[img_id] = image
    elif args[0] == 'draw':
        # Draw image from local cache.
        _, pos, img_id = args
        image = images[img_id]
        screen.blit(image, tuple(pos))
    elif args[0] == 'end':
        # End frame.
        pygame.display.flip()
        screen.fill((255, 255, 255))
        pygame.event.pump()

        # Send currently pressed keys to server.
        data = json.dumps(pygame.key.get_pressed())
        sock_file.write(data + '\n')
        sock_file.flush()
