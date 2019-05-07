package main

// Server file contains the server and game initialization
// Written by Joakim Loxdal 2019

import (
	"flag"
	"log"
	"net"
	"strconv"
)

func main() {
	port := flag.Int("port", 3333, "Connection port")
	flag.Parse()

	l, err := net.Listen("tcp", ":"+strconv.Itoa(*port))
	if err != nil {
		log.Panicln(err)
	}
	log.Println("Listening to connections on port", strconv.Itoa(*port))
	defer l.Close()

	game := Game{}
	game.Name = "The first game"
	game.isStarted = false
	game.Players = make(map[string]User)
	game.Items = make(map[int]Item)
	game.Map = createRandomMap(32)
	go game.gameHandler()

	for {
		conn, err := l.Accept()
		if err != nil {
			log.Panicln(err)
		}
		go userHandler(conn, &game)
	}
}
