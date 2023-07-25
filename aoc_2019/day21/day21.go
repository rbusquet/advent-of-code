package day21

import (
	"fmt"

	"github.com/rbusquet/advent-of-code/aoc_2019/computer"
)

func part1() {
	input := make(chan int)
	output := computer.RunProgram("./2019/day21/input.txt", input, computer.NOOP)
	program := []string{
		"NOT A J",
		"NOT C T",
		"AND D T",
		"OR T J",
		"WALK",
	}

	quit := make(chan int)
	go func() {
		for out := range output {
			if out > 127 {
				fmt.Println(out)
				break
			}
			// fmt.Print(string(out))
		}
		quit <- 1
	}()
	for _, line := range program {
		for _, char := range line {
			input <- int(char)
		}
		input <- 10
	}
	<-quit
}

func part2() {
	input := make(chan int)
	output := computer.RunProgram("./2019/day21/input.txt", input, computer.NOOP)
	program := []string{
		"NOT C T", // T = !C,                 J = false
		"NOT B J", // T = !C,                 J = !B
		"OR T J",  // T = !C,                 J = !C || !B
		"NOT A T", // T = !A,                 J = !C || !B
		"OR T J",  // T = !A,                 J = !A || !C || !B
		"OR E T",  // T = E || !A             J = !A || !C || !B
		"OR H T",  // T = H || E || !A        J = !A || !C || !B
		"AND D T", // T = D & (H || E || !A)  J = !A || !C || !B
		"AND T J", // T = D & (H || E || !A)  J = D & (H || E || !A) & (!A || !C || !B)
		"RUN",
	}

	quit := make(chan int)
	go func() {
		for out := range output {
			if out > 127 {
				fmt.Println(out)
				break
			}
			fmt.Print(fmt.Sprint(out))
		}
		quit <- 1
	}()
	for _, line := range program {
		for _, char := range line {
			input <- int(char)
		}
		input <- 10
	}
	<-quit
}

// Run day 21
func Run() {
	fmt.Println("-- Day21 --")
	fmt.Print("Part one output: ")
	part1()
	fmt.Print("Part two output: ")
	part2()
}
