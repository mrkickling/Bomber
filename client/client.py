import socket
import time
from response_handler import ResponseHandler
from game import Game
from graphics_handler import GraphicsHandler
from input_handler import InputHandler
from shooter_protocol import Methods
import pygame

# File is the main file of the client, handles connection, initialization and running of methods
# Joakim Loxdal 2019

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 3333        # The port used by the server
USERNAME = input("What's your name?")

response_handler = ResponseHandler()
game = Game(USERNAME)
input_handler = InputHandler()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	request = bytes([Methods.READY]) + USERNAME.encode()
	s.sendall(request) # Logga in

	while(not game.is_running):
		response_handler.handle_response(s, game)

	graphics_handler = GraphicsHandler(game)

	while(game.is_running):
		response_handler.handle_response(s, game)
		input_handler.processInput(s, game)
		if len(game.map):
			graphics_handler.render_game(game)
		if(not game.is_started):
			graphics_handler.render_wait_screen()
