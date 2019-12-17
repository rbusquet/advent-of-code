package main

import (
	"advent-of-code/2019/utils"
	"fmt"
	"strconv"
	"time"

	"github.com/gdamore/tcell"
)

// TileType is an int
type TileType int

const (
	empty TileType = iota
	wall
	block
	paddle
	ball
)

// Tile holds tile position
type Tile struct {
	x, y int
}

func part1() {
	program := utils.ReadProgram("./input.txt")
	input := make(chan int)
	computer := utils.NewComputer(&program, input)
	output := computer.GetOutput()
	go computer.Execute()

	objects := make(map[Tile]TileType)

	for x := range output {
		y := <-output
		id := TileType(<-output)
		tile := Tile{x, y}
		objects[tile] = id
	}

	countBlocks := 0

	for _, tileID := range objects {
		if tileID == block {
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

	quit := make(chan struct{})

	maxX := 0
	maxY := 0
	pressed := 0
	screen, err := tcell.NewScreen()
	screen.Init()
	if err != nil {
		panic(err)
	}
	// fmt.Println("Accepted first input")
	// input <- 0
	tick := time.Tick(3)

	go func() {
		for {
			select {
			case <-tick:
				{
					select {
					case input <- pressed:
						pressed = 0
					default:
						continue
					}
				}
			case x := <-output:
				{
					y := <-output
					if x == -1 {
						v := strconv.Itoa(<-output)
						for _, r := range v {
							screen.SetContent(y, 0, r, nil, 0)
							y++
						}
						break
					}
					if x > maxX {
						maxX = x
					}
					if y > maxY {
						maxY = y
					}
					id := TileType(<-output)
					cell := ' '
					sync := false
					switch id {
					case empty:
						cell = ' '
					case wall:
						cell = 'X'
					case block:
						cell = 'X'
					case paddle:
						{
							cell = '_'
						}

					case ball:
						{
							cell = 'o'
							sync = true
						}
					}
					screen.SetContent(x, y+1, cell, nil, 0)
					if sync {
						time.Sleep(time.Second)
						screen.Sync()
					}

				}
			}
		}
	}()

	go func() {
		for {
			ev := screen.PollEvent()
			switch ev := ev.(type) {
			case *tcell.EventKey:
				switch ev.Key() {
				case tcell.KeyEscape, tcell.KeyEnter:
					close(quit)
					return
				case tcell.KeyCtrlL:
					screen.Sync()
				}
				switch ev.Rune() {
				case 'j':
					pressed = -1
				case 'k':
					pressed = 0
				case 'l':
					pressed = 1
				}
			case *tcell.EventResize:
				screen.Sync()
			}
		}
	}()
	<-quit
	screen.Fini()
}
