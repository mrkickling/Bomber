import pygame
import math

# File contains handling of user input
# Joakim Loxdal 2019

key_to_move = {
	pygame.K_DOWN: {"x":0, "y":1},
	pygame.K_UP: {"x":0, "y":-1},
	pygame.K_LEFT: {"x":-1, "y":0},
	pygame.K_RIGHT: {"x":1, "y":0},
}

class InputHandler:

	def __init__(self):
		pass

	def processInput(self, socket, game):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game.is_running = False
			elif event.type == pygame.KEYDOWN:
				if event.key in key_to_move:
					move = key_to_move[event.key]
					game.walking_direction = move
					game.move(socket, move['x'], move['y'])
				elif event.key == pygame.K_SPACE:
					game.shoot(socket)
