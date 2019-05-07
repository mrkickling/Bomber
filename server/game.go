package main

// Game file contains game logic
// Written by Joakim Loxdal 2019

import (
	"log"
	"math"
	"math/rand"
	"time"
)

// Map struct represents a map and its size
type Map struct {
	Tiles []byte
	Size  int
}

// Game struct representing a game
type Game struct {
	Name      string
	Map       Map
	Players   map[string]User
	Items     map[int]Item
	isStarted bool
}

// ItemType enum representing different item types
type ItemType int

// GUN, FLASH is ItemTypes
const (
	BOMBITEM   ItemType = 0
	PLACEDBOMB ItemType = 1
)

// Item struct representing an item inside a game map
type Item struct {
	Type ItemType
	ID   int
	X    int
	Y    int
}

// Add item to game struct
func (g *Game) gameHandler() {
	for true {
		if len(g.Players) > 1 && !g.isStarted {
			g.startGame()
		} else if len(g.Players) <= 1 {
			g.isStarted = false
		}
	}
}

// Add item to game struct
func (g *Game) addItem(itemType ItemType, id int, x int, y int) Item {
	newItem := Item{itemType, id, x, y}
	g.Items[id] = newItem
	return newItem
}

func (g *Game) takeItem(id int, player *User) {
	player.Shots = player.Shots + 1
	delete(g.Items, id)
	for _, p := range g.Players {
		p.itemPos(*g)
		p.playerPos(*g)
	}
}

// Add user to game struct
func (g *Game) addUser(user User) {
	g.Players[user.Name] = user
	user.maptiles(*g)
	for _, player := range g.Players {
		player.playerPos(*g)
	}
	if g.isStarted {
		user.start()
	}
}

// Returns: true, item-id if position contains an item, otherwise: false, 0
func (g *Game) positionHasItem(pos int) (bool, int) {
	x := pos % g.Map.Size
	y := pos / g.Map.Size
	itemOnPos := false
	id := 0
	for _, item := range g.Items {
		if item.X == x && item.Y == y {
			itemOnPos = true
			id = item.ID
		}
	}
	return itemOnPos, id
}

// returns true if position contains user or wall
func (g *Game) positionIsOccupied(pos int) bool {
	x := pos % g.Map.Size
	y := pos / g.Map.Size
	userOnPos := false
	for _, player := range g.Players {
		if player.X == x && player.Y == y {
			userOnPos = true
		}
	}
	return (userOnPos || g.Map.Tiles[pos] == byte(1))
}

// Get a random empty position
func (g *Game) getRandomEmptyPosition() (int, int) {
	found := false
	for !found {
		newPos := rand.Intn(g.Map.Size * g.Map.Size) // Finds a random position not occupied
		if !g.positionIsOccupied(newPos) {
			x := newPos % g.Map.Size
			y := newPos / g.Map.Size
			return x, y
		}
	}
	return 0, 0
}

// Add user to game struct
func (g *Game) deleteUser(user *User) {
	delete(g.Players, (*user).Name)
	log.Println("Deleted user " + (*user).Name)
}

// Move user with delta-x and delta-y
func (g *Game) moveUser(player *User, deltaX float64, deltaY float64) {
	newX := player.X + int(deltaX)
	newY := player.Y + int(deltaY)
	newPos := newX + newY*g.Map.Size

	if math.Abs(deltaX) > 1 || math.Abs(deltaY) > 1 {
		player.error([]byte("Illegal move: Moving to fast"))
		return
	} else if newX > g.Map.Size || newY > g.Map.Size {
		player.error([]byte("Illegal move: Move out of map"))
		return
	} else if g.positionIsOccupied(newPos) {
		player.error([]byte("Illegal move: Occupied tile"))
		return
	}
	hasItems, id := g.positionHasItem(newPos)
	if hasItems {
		g.takeItem(id, player)
	}
	player.X = newX
	player.Y = newY
	g.Players[player.Name] = *player

	for _, p := range g.Players {
		p.playerPos(*g)
	}
}

func (g *Game) placeBomb(x int, y int) {
	bomb := g.addItem(PLACEDBOMB, rand.Intn(255), x, y)
	log.Println("Placed bomb")
	go g.explodeBomb(bomb)
	for _, player := range g.Players {
		player.itemPos(*g)
	}
}

// Create a random map with walls and void
func createRandomMap(size int) Map {
	newMap := mapArray
	for tile := 0; tile < size*size; tile++ {
		if tile < size || tile > size*size-size {
			newMap[tile] = 1 // top/bottom wall
		}
		if tile%size == 0 || tile%size == size-1 {
			newMap[tile] = 1 // left/right wall
		}
	}
	return Map{newMap, size}
}

// Spawn items on random locations
func (g *Game) spawnRandomItems(size int) {
	for i := 0; i < size; i++ {
		id := len(g.Items)
		x, y := g.getRandomEmptyPosition()
		g.addItem(BOMBITEM, id, x, y)
	}
}

// Explode the bomb after 4 seconds and kill users who are in blast area
func (g *Game) explodeBomb(bomb Item) {
	time.Sleep(4 * time.Second)
	xMin := 0
	xMax := g.Map.Size + 1
	yMin := 0
	yMax := g.Map.Size + 1

	// Find x min and x max, y min and y max of explosion area
	for i := 0; i < int(g.Map.Size); i++ {
		if g.Map.Tiles[bomb.Y*g.Map.Size+i] == byte(1) { // When a wall is found in x-Direction
			if i < bomb.X { // When last wall is found to the left of the bomb, set xMin
				xMin = i
			} else if i > bomb.X && xMax > g.Map.Size { // When first wall was found to the right of the bomb, set xMax
				xMax = i
			}
		}
		if g.Map.Tiles[i*g.Map.Size+bomb.X] == byte(1) { // When a wall is found in y-Direction
			if i < bomb.Y { // When last wall is found above the bomb, set yMin
				yMin = i
			} else if i > bomb.Y && yMax > g.Map.Size { // When first wall is found below the bomb, set yMax
				yMax = i
			}
		}
	}

	// Find out which users to kill with explosion
	for _, player := range g.Players {
		if (player.X > xMin && player.X < xMax && player.Y == bomb.Y) ||
			(player.Y > yMin && player.Y < yMax && player.X == bomb.X) {
			player.gameover("You lost.")
			delete(g.Players, player.Name)
			break
		}
	}
	// If only one person is left, let them win
	if len(g.Players) == 1 {
		for _, player := range g.Players {
			player.gameover("You won!")
			g.resetGame()
		}
	}
	// Delete bomb
	delete(g.Items, bomb.ID)
}

// Start the game and spawn items
func (g *Game) startGame() {
	g.isStarted = true
	g.spawnRandomItems(len(g.Players) * 3)
	for _, player := range g.Players {
		player.start()
		player.itemPos(*g)
	}
}

// Reset game
func (g *Game) resetGame() {
	g.Items = make(map[int]Item)
	for _, player := range g.Players {
		player.itemPos(*g)
	}
}
