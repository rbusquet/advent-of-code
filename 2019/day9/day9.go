package day9

import (
	"advent-of-code/2019/utils"
	"fmt"
)

func run(input int) {
	memory := utils.ReadProgram("./day9/input.txt")

	computer := utils.NewComputer(&memory, input)

	for {
		output, code := computer.Execute()
		if code == "OUTPUT" {
			fmt.Println(output)
		} else if code == "HALT" {
			break
		}
	}
}

// Run day 9
func Run() {
	fmt.Println("-- Day 9 --")
	fmt.Print("Part one output: ")
	run(1)
	fmt.Print("Part two output: ")
	run(2)
}
