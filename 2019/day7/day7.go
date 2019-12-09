package day7

import (
	"advent-of-code/2019/utils"
	"fmt"
	"strconv"
)

// Amplifier is each of the thrust amplifiers of the ship
type Amplifier struct {
	computer *utils.Computer
}

// NewAmplifier returns Amplifier
func NewAmplifier(program []int, input int) Amplifier {
	cp := append([]int{}, program...)
	computer := utils.NewComputer(&cp, input)
	return Amplifier{&computer}
}

func (a *Amplifier) step() (output int, code string) {
	return a.computer.Execute()
}

func (a *Amplifier) setInput(input int) {
	a.computer.SetInput(input)
}

func (a *Amplifier) getOutput() int {
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
	}
	fmt.Println("Part two result:", currentResult)
}

func readProgram(filename string) []int {
	memory := []int{}
	scanner := utils.GenerateCommaSeparatedScanner(filename)
	for scanner.Scan() {
		if val, err := strconv.Atoi(scanner.Text()); err == nil {
			memory = append(memory, val)
		}
	}
	return memory
}

func runConfig(config []int) int {
	memory := readProgram("./day7/input.txt")
	input := 0
	code := ""
	for _, phase := range config {
		amplifier := NewAmplifier(memory, phase)
		amplifier.step()
		amplifier.setInput(input)
		for {
			input, code = amplifier.step()
			if code == "HALT" {
				break
			}
		}
	}
	return input
}

func runLoop(config []int) int {
	memory := readProgram("./day7/input.txt")
	input := 0
	cycle := 0
	code := ""
	amplifiers := make(map[int]*Amplifier)

	halted := make(map[int]bool)

	for {
		if len(halted) == len(config) {
			break
		}
		i := cycle % len(config)
		if halted[i] {
			cycle++
			continue
		}

		phase := config[i]

		_, exists := amplifiers[i]
		if !exists {
			amp := NewAmplifier(memory, phase)
			amp.step()
			amplifiers[i] = &amp
		}
		amplifier := amplifiers[i]
		amplifier.setInput(input)
		for {
			input, code = amplifier.step()
			if code == "OUTPUT" {
				break
			}
			if code == "HALT" {
				halted[i] = true
				break
			}
		}

		cycle++
	}
	return input
}
