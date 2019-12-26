package day7

import (
	"fmt"

	"github.com/rbusquet/advent-of-code/utils"
)

// Amplifier is each of the thrust amplifiers of the ship
type Amplifier struct {
	computer *utils.Computer
	input    chan int
}

// NewAmplifier returns Amplifier
func NewAmplifier(program []int, input chan int) Amplifier {
	cp := append([]int{}, program...)
	computer := utils.NewComputer(&cp, input)
	return Amplifier{&computer, input}
}

func (a *Amplifier) output() chan int {
	return a.computer.GetOutput()
}

// Run day 7
func Run() {
	fmt.Println("-- Day 7 --")
	currentResult := 0
	for _, config := range utils.Permutations([]int{0, 1, 2, 3, 4}, 5) {
		result := runConfig(config)
		// fmt.Printf("config %d returned %d\n", config, result)
		if result > currentResult {
			currentResult = result
		}
	}
	fmt.Println("Part one result:", currentResult)

	currentResult = 0
	for _, config := range utils.Permutations([]int{5, 6, 7, 8, 9}, 5) {
		result := runLoop(config)
		// fmt.Printf("config %d returned %d\n", config, result)
		if result > currentResult {
			currentResult = result
		}
		// break
	}
	fmt.Println("Part two result:", currentResult)
}

func runConfig(config []int) int {
	memory := utils.ReadProgram("./day7/input.txt")
	input := 0
	in := make(chan int)
	for _, phase := range config {
		amplifier := NewAmplifier(memory, in)
		go amplifier.computer.Execute()
		amplifier.input <- phase
		amplifier.input <- input
		input = <-amplifier.output()
	}
	return input
}

func runLoop(config []int) int {
	memory := utils.ReadProgram("./day7/input.txt")

	entry := make(chan int)
	lastOutput := entry

	for _, phase := range config {
		input := make(chan int)
		amplifier := NewAmplifier(memory, input)
		go amplifier.computer.Execute()
		input <- phase
		go amplifier.pipe(lastOutput)
		lastOutput = amplifier.output()
	}
	entry <- 0

	var o int

	for o = range lastOutput {
		entry <- o
	}
	return o
}

func (a *Amplifier) pipe(entry chan int) {
	for value := range entry {
		a.input <- value
	}
	close(a.input)
}
