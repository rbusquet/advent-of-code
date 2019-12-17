package main

import (
	"advent-of-code/2019/utils"
	"fmt"
)

type TileType int

const (
	empty TileType = iota
	wall
	block
	paddle
	ball
)

type Tile struct {
	id   TileType
	x, y int
}

func part1() {
	program := utils.ReadProgram("./input.txt")
	input := make(chan int)
	computer := utils.NewComputer(&program, input)
	output := computer.GetOutput()
	go computer.Execute()

	objects := []Tile{}

	for x := range output {
		y := <-output
		id := TileType(<-output)
		tile := Tile{id, x, y}
		objects = append(objects, tile)
	}

	countBlocks := 0

	for _, tile := range objects {
		if tile.id == block {
			countBlocks++
		}
	}
	fmt.Println(countBlocks)
}

func main() {
	program := utils.ReadProgram("./input.txt")
	program[0] = 2

	input := make(chan int)
	computer := utils.NewComputer(&program, input)
	output := computer.GetOutput()
	go computer.Execute()

	objects := []Tile{}

	maxX := 0
	maxY := 0

	for x := range output {
		y := <-output
		if x > maxX {
			maxX = x
		}
		if y > maxY {
			maxY = y
		}
		id := TileType(<-output)
		tile := Tile{id, x, y}
		objects = append(objects, tile)
	}
}
