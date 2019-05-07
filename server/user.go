package main

// User file contains user initialization and user input handling
// Written by Joakim Loxdal 2019

import (
	"log"
	"net"
)

// User is a struct defining user
type User struct {
	Name       string
	Shots      int
	Connection net.Conn
	X          int
	Y          int
}

// Creates the user and handles connection and starts the input handler
func userHandler(conn net.Conn, game *Game) {
	user := User{}
	user.Connection = conn
	user.Name = ""
	user.Shots = 0
	x, y := game.getRandomEmptyPosition()
	user.X = x
	user.Y = y

	log.Println("Accepted new connection.")
	user.inputHandler(game, conn)

	defer conn.Close()
	defer game.deleteUser(&user)
}

// Handles input sent from the client to the server
func (user *User) inputHandler(game *Game, conn net.Conn) {
	for {
		buf := make([]byte, 1024)
		size, err := conn.Read(buf)
		if err != nil {
			return
		}
		data := buf[:size]
		log.Println("Received new data from user " + user.Name + ": ")

		request := parseRequest(data)
		// Handle requests
		switch request.Type {
		case READY:
			if user.Name == "" {
				log.Println(string(request.Data) + " is now a connected user")
				user.Name = string(request.Data)
				game.addUser(*user)
				user.success()
			} else {
				user.error([]byte("You are already registered."))
			}
		case MOVE:
			if game.isStarted && user.Name != "" {
				deltaX := int8(request.Data[0])
				deltaY := int8(request.Data[1])
				game.moveUser(user, float64(deltaX), float64(deltaY))
			} else if user.Name == "" {
				user.error([]byte("Your user is not registered yet"))
			} else {
				user.error([]byte("The game has not started yet"))
			}
		case SHOT:
			if user.Shots > 0 {
				x := int(request.Data[0])
				y := int(request.Data[1])
				game.placeBomb(x, y)
				user.Shots--
			}
		case ERROR:
			user.error(request.Data)
		}

	}
}
