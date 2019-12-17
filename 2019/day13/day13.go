package day13

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
	program := utils.ReadProgram("./day13/input.txt")
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

func part2() {
	program := utils.ReadProgram("./day13/input.txt")
	program[0] = 2

	input := make(chan int)
	computer := utils.NewComputer(&program, input)

	output := computer.GetOutput()

	go computer.Execute()

	quit := make(chan struct{})

	pressed := 0
	screen, err := tcell.NewScreen()
	if err != nil {
		panic(err)
	}
	screen.Init()
	scoreVal := ""

	var p Tile
	createdB := false
	go func() {
		for {
			select {
			case input <- pressed:
				screen.Show()
				pressed = 0
			case x := <-output:
				y := <-output
				if x == -1 {
					v := strconv.Itoa(<-output)
					scoreVal = v
					for _, r := range v {
						screen.SetContent(y, 0, r, nil, 0)
						y++
					}
					break
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
					cell = tcell.RuneBlock
				case paddle:
					cell = tcell.RuneBlock
					p = Tile{x, y}
				case ball:
					cell = '@'
					sync = true
					if !createdB {
						createdB = true
					} else {
						// sprinkle some AI...
						if x < p.x {
							pressed = -1
						} else if x >= p.x {
							pressed = 1
						}
					}
				}

				screen.SetContent(x, y+1, cell, nil, 0)
				if sync {
					time.Sleep(time.Second / 1000)
					screen.Show()
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
				}
			case *tcell.EventResize:
				screen.Sync()
			}
		}
	}()
	<-quit
	fmt.Println("score:", scoreVal)
	screen.Fini()
}

// Run day 13
func Run() {
	fmt.Println("-- Day 13 --")
	fmt.Print("Part one output:")
	part1()
	fmt.Print("Part two output:")
	part2()
}
