package day19

import (
	"advent-of-code/2019/utils"
	"fmt"
)

func noop(x []int) []int {
	return x
}

func drone(x, y int) int {
	input := make(chan int)
	output := utils.RunProgram("./day19/input.txt", input, noop)
	input <- x
	input <- y
	return <-output
}

func asyncDrone(x, y int, out chan int, buffer chan int) {
	buffer <- 1
	status := drone(x, y)
	out <- status
	<-buffer
}

func part1() {
	count := 0
	buffer := make(chan int, 10)
	sumOutput := make(chan int, 50)
	for x := 0; x < 50; x++ {
		for y := 0; y < 50; y++ {
			go asyncDrone(x, y, sumOutput, buffer)
		}
	}
	responses := 0
	for x := range sumOutput {
		count += x
		responses++
		if responses == 50*50 {
			break
		}
	}
	fmt.Println(count)
}

func part2() {
	lastX := 0
loop:
	for y := 100; ; y++ {
		for x := lastX; ; x++ {
			status := drone(x, y)
			if status == 1 {
				lastX = x
				otherEdges := []utils.Position{
					utils.NewPosition(x, y-99),
					utils.NewPosition(x+99, y-99),
					utils.NewPosition(x+99, y),
				}
				for _, pos := range otherEdges {
					if drone(pos.GetX(), pos.GetY()) == 0 {
						continue loop
					}
				}
				fmt.Println(x*10000 + y - 99)
				return
			}
		}
	}
}

// Run day 19
func Run() {
	fmt.Println("-- Day 19 --")
	fmt.Print("Part one output: ")
	part1()
	fmt.Print("Part two output: ")
	part2()
}
