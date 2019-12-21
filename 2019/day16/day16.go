package day16

import (
	"advent-of-code/2019/utils"
	"fmt"
	"strconv"
)

func singleOutput(index int, input []int64) int64 {
	pattern := []int64{0, 1, 0, -1}
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
	sum := int64(0)

	for _, x := range input {
		m := <-multiplier
		sum += x * pattern[m%4]
	}
	quit <- 1

	return utils.AbsInt(sum) % 10
}

func part1() {
	scanner := utils.DigitSeparatedScanner("./day16/input.txt")

	input := []int64{}
	for scanner.Scan() {
		x, _ := strconv.Atoi(scanner.Text())
		input = append(input, int64(x))
	}
	inputSize := len(input)

	for phase := 0; phase < 100; phase++ {
		output := []int64{}
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
