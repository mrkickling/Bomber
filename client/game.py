from shooter_protocol import Methods
from time import time
import math

# File contains game information (maps, users, items) that will be rendered
# Joakim Loxdal 2019

class Game:

	# game constructor
	def __init__(self, username):
		self.username = username
		self.map = []
		self.users = {}
		self.items = {}
		self.is_running = False
		self.is_started = False
		self.walking_direction = {"x":0, "y":0}
		self.game_is_over = False
		self.end_credit = ""

	def start_game(self):
		self.is_started = True

	def game_over(self, message):
		print("Game is set to over")
		self.game_is_over = True
		self.end_credit = message
		self.users = {}
		self.items = {}

	# Parse user name and user position
	def parseUserPos(self, x, y, name, shots):
		self.users[name] = {"name":name, "x":x, "y":y, "shots":int(shots)}
		print(shots)

	# Parse user name and user position
	def parseItemPos(self, x, y, type, id):
		item = {"type":type, "id":id, "x":x, "y":y, "added":int(time())}
		self.items[id] = item

	# Find the area where the explosion will be
	def get_explosion_area(self, bomb):
		map_size = int(math.sqrt(len(self.map)))
		xMin = 0
		xMax = map_size
		yMin = 0
		yMax = map_size
		# Find x min and x max of explosion area
		for x in range(map_size):
			if self.map[bomb['y']*map_size + x] == 1:
				if x < bomb['x']:
					xMin = x
				elif x > bomb['x']:
					xMax = x
					break

		# Find y min and y max of explosion area
		for y in range(map_size):
			if self.map[y*map_size + bomb['x']] == 1:
				if y < bomb['y']:
					yMin = y
				elif y > bomb['y']:
					yMax = y
					break

		return({"xMin":xMin, "xMax":xMax, "yMin":yMin,"yMax":yMax})


	# Fills the map with 1 (wall) or 0 (void)
	def parseMap(self, data):
		for tile in data:
			self.map.append(int(tile))
		print("Map size:", len(self.map))
		self.is_running = True

	def move(self, s, x, y):
		x = x.to_bytes( 1 , byteorder='big' , signed=True )
		y = y.to_bytes( 1 , byteorder='big' , signed=True )
		request = bytes([Methods.MOVE]) + x + y
		s.sendall(request)

	def shoot(self, s):
		request = bytes([Methods.SHOT, self.users[self.username]['x'], self.users[self.username]['y']])
		s.sendall(request)
