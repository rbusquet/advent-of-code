package day15

import (
	"advent-of-code/2019/utils"
	"fmt"
)

func part1() []int {
	program := utils.ReadProgram("./day15/input.txt")
	input := make(chan int)
	computer := utils.NewComputer(&program, input)
	output := computer.GetOutput()
	go computer.Execute()

	queue := []int{}

	pos := utils.NewPosition(0, 0)
	reversed := map[int]int{
		1: 2,
		2: 1,
		3: 4,
		4: 3,
	}
	visited := make(map[utils.Position]bool)
loop:
	for {
		for direction := 1; direction < 5; direction++ {
			next := nextPosition(direction, pos)
			if visited[next] {
				continue
			}
			visited[next] = true
			input <- direction
			status, ok := <-output
			if !ok {
				return queue
			}
			switch status {
			case 1:
				pos = next
				queue = append(queue, direction)
				continue loop
			case 2:
				return queue
			}

		}

		back := queue[len(queue)-1]
		queue = queue[:len(queue)-1]
		back = reversed[back]
		input <- back
		<-output
		pos = nextPosition(back, pos)
	}
}

func nextPosition(direction int, pos utils.Position) utils.Position {
	x, y := pos.GetX(), pos.GetY()
	switch direction {
	case 1:
		y--
	case 2:
		y++
	case 3:
		x++
	case 4:
		x--
	}
	return utils.NewPosition(x, y)
}

// Run day 15
func Run() {
	fmt.Println("-- Day 15 --")
	fmt.Print("Part one output: ")
	queue := part1()
	fmt.Println(len(queue) + 1)
}
