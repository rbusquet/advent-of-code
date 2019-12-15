package day9

import (
	"advent-of-code/2019/utils"
	"fmt"
)

func run(input int) {
	memory := utils.ReadProgram("./day9/input.txt")

	entry := make(chan int)

	computer := utils.NewComputer(&memory, entry)
	go computer.Execute()
	entry <- input

	result := 0
	for o := range computer.GetOutput() {
		result = o
	}
	fmt.Println(result)
}

// Run day 9
func Run() {
	fmt.Println("-- Day 9 --")
	fmt.Print("Part one output: ")
	run(1)
	fmt.Print("Part two output: ")
	run(2)
}
