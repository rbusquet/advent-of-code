package day17

import (
	"fmt"

	"github.com/rbusquet/advent-of-code/utils"
)

func part1() {
	program := utils.ReadProgram("./day17/input.txt")
	input := make(chan int)
	computer := utils.NewComputer(&program, input)
	output := computer.GetOutput()

	go computer.Execute()

	space := make(map[utils.Position]int)
	scaffolds := []utils.Position{}

	x, y := 0, 0
	for out := range output {
		if out == 10 {
			x++
			y = 0
			continue
		}
		pos := utils.NewPosition(x, y)
		space[pos] = out
		if out == 35 {
			scaffolds = append(scaffolds, pos)
		}
		y++
	}

	sum := 0
loop:
	for _, scaffold := range scaffolds {
		for pos := range scaffold.Surrounds() {
			what := space[pos]
			if what != 35 {
				continue loop
			}
		}
		// all around are scaffolds
		sum += scaffold.GetX() * scaffold.GetY()
	}
	fmt.Println(sum)
}

func readLine(output chan int) {
	for out := range output {
		// fmt.Print(string(out))
		if out == '\n' {
			break
		}
	}
}

func writeLine(input chan int, line string) {
	for _, x := range line {
		input <- int(x)
	}
	input <- 10
}

func part2() {
	// Instructions:
	// A,A,B,C,A,C,B,C,A,B

	// A: L,4,L,10,L,6
	// B: L,6,L,4,R,8,R,8
	// C: L,6,R,8,L,10,L,8,L,8
	input := make(chan int)
	preprocess := func(prog []int) []int {
		prog[0] = 2
		return prog
	}
	output := utils.RunProgram("./day17/input.txt", input, preprocess)
	// print grid
	skippedLine := false
	for out := range output {
		if out == '\n' {
			if skippedLine {
				break
			}
			skippedLine = true
		} else {
			skippedLine = false
		}
	}

	lines := []string{
		"A,A,B,C,A,C,B,C,A,B",
		"L,4,L,10,L,6",
		"L,6,L,4,R,8,R,8",
		"L,6,R,8,L,10,L,8,L,8",
	}
	for _, line := range lines {
		readLine(output)
		writeLine(input, line)
	}
	readLine(output)
	writeLine(input, "n")

	res := 0
	skippedLine = false
	for out := range output {
		res = out
	}
	fmt.Println(res)
}

// Run day 17
func Run() {
	fmt.Println("-- Day 17 --")
	fmt.Print("Part one output: ")
	part1()
	fmt.Print("Part two output: ")
	part2()
}
