package main

// Shooter Protocol file contains all protocol specific methods and request parsing
// Written by Joakim Loxdal 2019

import "log"

// All methods (both client and server)
const (
	MOVE      byte = 1   // Received from users requesting a move (in x and y direction)
	START     byte = 2   // Send game start symbol
	MAPTILES  byte = 3   // Send map to clients
	PLAYERPOS byte = 4   // Send players and their positions
	ITEMPOS   byte = 5   // Send items and their positions
	SUCCESS   byte = 6   // Sent when a response from the client was understood and executed
	SHOT      byte = 7   // Received when a shot was fired by client, and is then returned to all users
	READY     byte = 8   // Received from user being ready to play
	GAMEOVER  byte = 9   // Send game over signal
	ERROR     byte = 255 // Send an error
)

// Request is a struct representing a request sent to server
type Request struct {
	Type byte
	Data []byte
}

// success is sent to client when client has sent a successful ready request
func (user User) success() {
	response := []byte{SUCCESS}
	user.Connection.Write(response)
}

// error is sent when a request from the client is unsuccessful
func (user User) error(message []byte) {
	response := append([]byte{ERROR}, message...)
	response = append(response, byte(0))
	user.Connection.Write(response)
}

// starting is sent to client when game starts
func (user User) start() {
	response := []byte{START}
	user.Connection.Write(response)
}

// starting is sent to client when game starts
func (user User) gameover(message string) {
	response := append([]byte{GAMEOVER}, message...)
	response = append(response, byte(0))
	user.Connection.Write(response)
}

// starting is sent to client when game starts
func (user User) shot(x int8, y int8) {
	response := []byte{SHOT, byte(x), byte(y)}
	user.Connection.Write(response)
}

// maptiles is sent to player
func (user User) maptiles(g Game) {
	response := append([]byte{MAPTILES, byte(g.Map.Size)}, []byte(g.Map.Tiles)...)
	user.Connection.Write(response)
}

//  all players position is sent to player
func (user User) playerPos(g Game) {
	response := []byte{PLAYERPOS, byte(len(g.Players))}
	for _, player := range g.Players {
		response = append(response, []byte(player.Name)...)
		response = append(response, []byte{byte(' '), byte(player.X), byte(player.Y), byte(player.Shots)}...)
	}
	user.Connection.Write(response)
}

//  all items positions is sent to a user
func (user User) itemPos(g Game) {
	response := append([]byte{ITEMPOS}, byte(len(g.Items)))
	for _, item := range g.Items {
		response = append(response, []byte{byte(item.Type), byte(item.ID), byte(item.X), byte(item.Y)}...)
	}
	user.Connection.Write(response)
}

// function used to parse data received from a client into a request struct
func parseRequest(data []byte) Request {
	commandLength := len(data)
	methodType := data[0]

	if commandLength < 1 {
		return Request{ERROR, []byte("Empty call.")}
	}

	args := data[1:commandLength]
	numArgumentsNeeded := 0

	switch methodType {
	case READY:
		numArgumentsNeeded = 2
	case MOVE:
		numArgumentsNeeded = 2
	case SHOT:
		numArgumentsNeeded = 2
	default:
		return Request{ERROR, []byte("Unknown method.")}
	}

	if len(args) < numArgumentsNeeded {
		return Request{ERROR, []byte("Too few arguments.")}
	}

	log.Println(methodType)

	return Request{methodType, args}
}
