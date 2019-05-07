from enum import Enum
import socket
import select
from shooter_protocol import Methods

# File contains handling of server response
# Joakim Loxdal 2019

int_to_enum = {
	1: Methods.MOVE,
	2: Methods.START,
	3: Methods.MAPTILES,
	4: Methods.PLAYERPOS,
	5: Methods.ITEMPOS,
	6: Methods.SUCCESS,
	7: Methods.SHOT,
	8: Methods.READY,
	9: Methods.GAMEOVER,
	255: Methods.ERROR,
}

class ResponseHandler:
	def handle_response(self, s, game): # Handle a response from the server
		ready = select.select([s], [], [], 0)
		if not ready[0]:
			return

		first_byte = s.recv(1)[0]
		command_type = int_to_enum[first_byte]

		if(command_type is Methods.SUCCESS):
			print("Success! You are registered.");

		if(command_type is Methods.START):
			print("Game is started");
			game.start_game()

		if(command_type is Methods.MAPTILES):
			print("Receiving maptiles")
			map_size = s.recv(1)[0]
			map = s.recv(map_size*map_size)
			game.parseMap(map)

		if(command_type is Methods.PLAYERPOS):
			print("Receiving Player positions")
			numUsers = s.recv(1)[0]
			for i in range(numUsers):
				user_name = ""
				nextChar = s.recv(1).decode("utf-8")[0]
				while nextChar is not ' ': # Hämta användarnamnet (avgränsas från resten med mellanrum)
					user_name += str(nextChar)
					nextChar = s.recv(1).decode("utf-8")[0]
				x = s.recv(1)[0]
				y = s.recv(1)[0]
				shots = s.recv(1)[0]
				user_name = user_name.replace('\x00', '')
				game.parseUserPos(x, y, user_name, shots)

		if(command_type is Methods.ITEMPOS):
			print("Receiving Item positions")
			numItems = s.recv(1)[0]
			game.items = {}
			for i in range(numItems):
				itemType = s.recv(1)[0]
				itemID = s.recv(1)[0]
				x = s.recv(1)[0]
				y = s.recv(1)[0]
				game.parseItemPos(x, y, itemType, itemID)

		if(command_type is Methods.ERROR):
			print("Receiving Error")
			message = ""
			char = s.recv(1)
			while char[0] is not 0:
				message += char.decode("utf-8")[0]
				char = s.recv(1)
			print("Error:", message);

		if(command_type is Methods.SHOT):
			print("Receiving BOMB")
			fromX = s.recv(1)
			fromY = s.recv(1)
			print("Bomb placed:", fromX, fromY);

		if(command_type is Methods.GAMEOVER):
			message = ""
			char = s.recv(1)
			while char[0] is not 0:
				message += char.decode("utf-8")[0]
				char = s.recv(1)

			print("Receiving GAME OVER:", message)
			game.game_over(message)
