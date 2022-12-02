package main

import (
	"fmt"

	"github.com/rbusquet/advent-of-code/2019/computer"
)

// main prints Ceci n'est pas une intcode program :)
func main() {
	input := make(chan int)
	output := computer.RunProgram("./2021/easteregg/program.txt", input, computer.NOOP)

	for out := range output {
		fmt.Print(string(rune(out)))
	}
}
