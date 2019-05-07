# File contains protocol methods
# Joakim Loxdal 2019

class Methods():
	MOVE 	   = 1
	START      = 2   # Reveive game start symbol
	MAPTILES   = 3   # Reveive map from server
	PLAYERPOS  = 4   # Reveive players and their positions
	ITEMPOS    = 5   # Receive items and their positions
	SUCCESS    = 6   # Received when a request from the was understood and executed by server
	SHOT 	   = 7   # Received when a shot was fired
	READY	   = 8   # Received when ready
	GAMEOVER   = 9   # Received when ready
	ERROR      = 255 # Receive an error

class ItemTypes():
	GUN = 0
	BOMB = 1
