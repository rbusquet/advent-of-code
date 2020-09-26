package day13

import (
	"fmt"
	"os"
	"strconv"
	"time"

	"github.com/gdamore/tcell"
	"github.com/rbusquet/advent-of-code/utils"
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

func part2(showScreen bool, speed int) {
	program := utils.ReadProgram("./day13/input.txt")
	program[0] = 2

	input := make(chan int)
	computer := utils.NewComputer(&program, input)

	output := computer.GetOutput()

	go computer.Execute()

	quit := make(chan struct{})

	pressed := 0
	var screen tcell.Screen
	if showScreen {
		s, err := tcell.NewScreen()
		if err != nil {
			panic(err)
		}
		screen = s
		screen.Init()
	}

	scoreVal := ""

	var p Tile
	var StyleDefault tcell.Style
	createdB := false
	go func() {
		for {
			select {
			case input <- pressed:
				if showScreen {
					screen.Show()
				}
				pressed = 0
			case x, ok := <-output:
				if !ok {
					close(quit)
					return
				}
				y := <-output
				if x == -1 {
					v := strconv.Itoa(<-output)
					scoreVal = v
					if showScreen {
						for _, r := range v {
							screen.SetContent(y, 0, r, nil, StyleDefault)
							y++
						}
					}
					break
				}
				id := TileType(<-output)
				cell := ' '
				// sync := false
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
					cell = 'x'
					// sync = true
					if !createdB {
						createdB = true
					} else {
						// sprinkle some AI...
						if x < p.x {
							pressed = -1
						} else if x > p.x {
							pressed = 1
						}
					}
					if showScreen {
						time.Sleep(time.Second / time.Duration(speed))
						screen.Show()
					}
				}
				if showScreen {
					screen.SetContent(x, y+1, cell, nil, StyleDefault)
				}
			}
		}
	}()

	if showScreen {
		go func() {
			for {
				ev := screen.PollEvent()
				switch ev := ev.(type) {
				case *tcell.EventKey:
					switch ev.Key() {
					case tcell.KeyEscape, tcell.KeyEnter, tcell.KeyCtrlC:
						close(quit)
						return
					}
				case *tcell.EventResize:
					screen.Sync()
				}
			}
		}()
	}
	<-quit
	if showScreen {
		screen.Fini()
	}
	fmt.Println(scoreVal)
}

// Run day 13
func Run() {
	showScreen := false
	speed := 200
	for idx, arg := range os.Args {
		if arg == "--show-arcade" {
			showScreen = true
			if len(os.Args) > idx+1 {
				if s, err := strconv.Atoi(os.Args[idx+1]); err != nil {
					panic(err)
				} else {
					speed = s
				}
			}
			break
		}
	}
	fmt.Println("-- Day 13 --")
	fmt.Print("Part one output: ")
	part1()
	fmt.Print("Part two output: ")
	part2(showScreen, speed)
}
