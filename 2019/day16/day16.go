package day16

import (
	"fmt"
	"strconv"

	"github.com/rbusquet/advent-of-code/2019/utils"
)

func singleOutput(index int, input []int) int {
	pattern := []int{0, 1, 0, -1}
	multiplier := make(chan int)
	quit := make(chan int)
	go func() {
		counter := 0
		for {
			idx := counter / (index + 1)
			select {
			case multiplier <- idx:
				counter++
			case <-quit:
				return
			}
		}
	}()

	<-multiplier // drop first one
	sum := 0

	for _, x := range input {
		m := <-multiplier
		sum += x * pattern[m%4]
	}
	quit <- 1

	return utils.AbsInt(sum) % 10
}

func part1() {
	file, scanner := utils.DigitSeparatedScanner("./day16/input.txt")
	defer (*file).Close()

	input := []int{}
	for scanner.Scan() {
		x, _ := strconv.Atoi(scanner.Text())
		input = append(input, int(x))
	}
	inputSize := len(input)

	for phase := 0; phase < 100; phase++ {
		output := []int{}
		for index := 0; index < inputSize; index++ {
			output = append(output, singleOutput(index, input))
		}
		input = output
	}
	for i, x := range input {
		fmt.Print(x)
		if i == 7 {
			break
		}
	}
}

// Run day 16
func Run() {
	fmt.Println("-- Day 16 --")
	fmt.Print("Part one output: ")
	part1()
	fmt.Println()
}
