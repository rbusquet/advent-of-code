package day11

import (
	"fmt"

	"github.com/rbusquet/advent-of-code/aoc_2019/computer"
	"github.com/rbusquet/advent-of-code/utils"
)

type color int

const (
	black color = iota
	white
)

type panel struct {
	position utils.Position
	color    color
}

type facing int

const (
	up facing = iota
	right
	down
	left
)

func run(initial color) map[utils.Position]*panel {
	program := computer.ReadProgram("./2019/day11/input.txt")

	input := make(chan int)
	computer := computer.NewComputer(&program, input)
	go computer.Execute()
	output := computer.GetOutput()
	colors := make(map[utils.Position]*panel)

	x := 0
	y := 0
	direction := up

	currenPosition := utils.NewPosition(x, y)
	colors[currenPosition] = &(panel{currenPosition, initial})

loop:
	for {
		currenPosition = utils.NewPosition(x, y)
		if _, exists := colors[currenPosition]; !exists {
			colors[currenPosition] = &(panel{currenPosition, black})
		}

		currentPanel := colors[currenPosition]

		select {
		case nextColor, ok := <-output:
			{
				if !ok {
					break loop
				}
				currentPanel.color = color(nextColor)

				turn := <-output
				if turn == 0 {
					direction--
				} else if turn == 1 {
					direction++
				}
				if direction < 0 {
					direction = left
				}
				if direction > 3 {
					direction = up
				}

				switch direction {
				case up:
					x--
				case right:
					y++
				case down:
					x++
				case left:
					y--
				}
			}
		case input <- int(currentPanel.color):
		}
	}
	return colors
}

func paint(colors map[utils.Position]*panel) {
	maxX := 0
	maxY := 0
	for pos := range colors {
		if maxX < pos.GetX() {
			maxX = pos.GetX()
		}
		if maxY < pos.GetY() {
			maxY = pos.GetY()
		}
	}
	for x := 0; x <= maxX+1; x++ {
		fmt.Println()
		for y := 0; y <= maxY+1; y++ {
			if panel, exists := colors[utils.NewPosition(x, y)]; exists {
				if panel.color == black {
					fmt.Print("  ")
				} else {
					fmt.Print("██")
				}
			} else {
				fmt.Print("  ")
			}
		}
	}
}

// Run day 11
func Run() {
	fmt.Println("-- Day 11 --")
	colors := run(black)
	fmt.Println("Part one output:", len(colors))
	colors = run(white)
	fmt.Println("Part two output:")
	paint(colors)
	fmt.Println()
}
