import pygame
import math
from shooter_protocol import ItemTypes
from time import time

# File contains all graphical rendering, using Pygame
# Joakim Loxdal 2019

# Screen settingsy
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640

# Colors used in graphicsHandler
BG_COLOR = (0,0,0)
WHITE = (255, 255, 255)
GRAY = (155, 155, 155)

# Images used
PLACED_BOMB_IMG = pygame.image.load('img/bombplaced.png')
BOMB_ITEM_IMG = pygame.image.load('img/bombitem.png')
USER_IMG = pygame.image.load('img/user.png')


class GraphicsHandler:
	loadingDots = 0

	def __init__(self, game):
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		pygame.display.set_caption('Shooter game progp')
		pygame.display.flip()
		self.game = game
		self.clock = pygame.time.Clock()

		self.map_size = math.sqrt(len(self.game.map))

		self.TILE_WIDTH = SCREEN_WIDTH/self.map_size
		self.TILE_HEIGHT = SCREEN_WIDTH/self.map_size

		self.PLACED_BOMB_IMG = pygame.transform.scale(PLACED_BOMB_IMG, (math.floor(self.TILE_WIDTH), math.floor(self.TILE_HEIGHT)))
		self.BOMB_ITEM_IMG = pygame.transform.scale(BOMB_ITEM_IMG, (math.floor(self.TILE_WIDTH), math.floor(self.TILE_HEIGHT)))
		self.USER_IMG = pygame.transform.scale(USER_IMG, (math.floor(self.TILE_WIDTH), math.floor(self.TILE_HEIGHT)))


	def render_wait_screen(self):
		# draw text
		font = pygame.font.Font(None, 25)
		dots = "."
		for i in range(GraphicsHandler.loadingDots):
			dots += "."
		text = font.render("Waiting for more users to connect" + dots, True, GRAY)
		text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
		self.screen.blit(text, text_rect)
		pygame.display.flip()
		GraphicsHandler.loadingDots = (GraphicsHandler.loadingDots+1)%3
		self.clock.tick(10)

	def render_gameover_screen(self, message):
		# draw text
		font = pygame.font.Font(None, 25)
		text = font.render(message, True, GRAY)
		text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
		self.screen.blit(text, text_rect)
		pygame.display.flip()

	def render_map(self, game):
		tile_index = 0
		for tile in game.map: # Draw game map
			column = tile_index % self.map_size
			row = math.floor(tile_index / self.map_size)
			if(tile == 1):
				pygame.draw.rect(self.screen, (200, 50, 50), [self.TILE_WIDTH * column,
								self.TILE_HEIGHT * row, self.TILE_WIDTH, self.TILE_HEIGHT])
			tile_index += 1

	def render_users(self, game):
		for name in game.users: # Draw users
			user = game.users[name]
			self.screen.blit(self.USER_IMG, (self.TILE_WIDTH * user['x'], self.TILE_HEIGHT * user['y']))

			font = pygame.font.Font(None, 20)
			# Text of username
			user_text = font.render(name, True, WHITE)
			user_text_rect = user_text.get_rect(center=(self.TILE_WIDTH * user['x'] + self.TILE_WIDTH/2,
								self.TILE_HEIGHT * user['y'] + 30))
			self.screen.blit(user_text, user_text_rect)

			# Text of number of shots
			shots_text = font.render(str(user['shots']), True, WHITE)
			shots_text_rect = shots_text.get_rect(center=(self.TILE_WIDTH * user['x'] + self.TILE_WIDTH/2,
								self.TILE_HEIGHT * user['y'] - self.TILE_HEIGHT/2))
			self.screen.blit(shots_text, shots_text_rect)

	def render_items(self, game):
		for id in game.items: # Draw items
			item = game.items[id]
			if item['type'] is ItemTypes.BOMB :
				deltaT = int(time()) - item['added']
				if(deltaT > 3 and  deltaT < 5):
					area = game.get_explosion_area(item)
					# Draw horizontal line
					pygame.draw.rect(self.screen, (0, 255, 0),
								[self.TILE_WIDTH * area['xMin'] + self.TILE_WIDTH,
								self.TILE_HEIGHT * item['y'] + self.TILE_HEIGHT/3,
								self.TILE_WIDTH * (area['xMax'] - area['xMin']) - self.TILE_WIDTH,
								self.TILE_HEIGHT/3])
					# Draw vertical line
					pygame.draw.rect(self.screen, (0, 255, 0),
								[self.TILE_WIDTH * item['x'] + self.TILE_WIDTH/3,
								self.TILE_HEIGHT * area['yMin'] + self.TILE_HEIGHT,
								self.TILE_WIDTH/3,
								self.TILE_HEIGHT * (area['yMax'] - area['yMin']) - self.TILE_WIDTH])
				elif(deltaT <= 3):
					self.screen.blit(self.PLACED_BOMB_IMG, (self.TILE_WIDTH * item['x'], self.TILE_HEIGHT * item['y']))
			else:
				self.screen.blit(self.BOMB_ITEM_IMG, (self.TILE_WIDTH * item['x'], self.TILE_HEIGHT * item['y']))

	def render_game(self, game):
		dt = self.clock.tick(30)

		self.screen.fill(BG_COLOR)


		if game.game_is_over:
			self.render_gameover_screen(game.end_credit)
		else:
			self.render_map(game)
			self.render_items(game)
			self.render_users(game)

		self.clock.tick(10)

		pygame.display.flip()
