package main

import (
	"fmt"

	"github.com/rbusquet/advent-of-code/utils"
)

func main() {
	inputs := make([]chan int, 50)
	computers := make([]*utils.Computer, 50)

	for i := 0; i < len(computers); i++ {
		program := utils.ReadProgram("./program.txt")
		input := make(chan int)
		computer := utils.NewComputer(&program, input)
		go computer.Execute()
		inputs[i] = input
		computers[i] = &computer
	}

	for i, input := range inputs {
		computer := computers[i]
		// process output
		fmt.Printf("Starting computer %d\n", i)
		go func(idx int, input chan int, c *utils.Computer) {
			input <- idx
			output := c.GetOutput()

			for {

				select {
				case input <- x:

				case dest, ok := <-output:
				}
			}

		}(i, input, computer)
	}

}
