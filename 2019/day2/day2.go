package day2

import (
	"advent-of-code/2019/utils"
	"fmt"
	"strconv"
)

func runProgram(noun int, verb int, memory ...int) []int {
	pos := 0
	memory[1] = noun
	memory[2] = verb
	for {
		opcode := memory[pos]
		if opcode == 99 {
			break
		}
		x := memory[pos+1]
		y := memory[pos+2]
		res := memory[pos+3]
		switch opcode {
		case 1:
			memory[res] = memory[x] + memory[y]
		case 2:
			memory[res] = memory[x] * memory[y]
		}
		pos = pos + 4
	}
	return memory
}

// Run day 2
func Run() {
	fmt.Println("-- Day 2 --")
	scanner := utils.GenerateCommaSeparatedScanner("./day2/input2.txt")
	memory := []int{}

	for scanner.Scan() {
		if val, err := strconv.Atoi(scanner.Text()); err != nil {
			panic(err)
		} else {
			memory = append(memory, val)
		}
	}
	input := make([]int, len(memory))
	copy(input, memory)
	endState := runProgram(12, 2, input...)
	fmt.Println("Part one output:", endState[0])

	for noun := 0; noun < 100; noun++ {
		for verb := 0; verb < 100; verb++ {
			copy(input, memory)
			if runProgram(noun, verb, input...)[0] == 19690720 {
				fmt.Println("Part two output:", 100*noun+verb)
				return
			}
		}
	}

}
