package computer

import (
	"github.com/rbusquet/advent-of-code/utils"
)

// Computer can run programs using IntCode defined in adventofcode.com/2019
type Computer struct {
	program        *[]int
	memory         *map[int]int
	input          chan int
	output         chan int
	pointer        int
	instruction    int
	relativeBase   int
	instructionSet map[int]func(*Computer)
}

// NewComputer instantiates a new computer object
func NewComputer(program *[]int, input chan int) Computer {
	memory := make(map[int]int)
	output := make(chan int)

	instructionSet := map[int]func(*Computer){
		1: add,
		2: multiply,
		3: readInput,
		4: writeOutput,
		5: jumpIfTrue,
		6: jumpIfFalse,
		7: lessThan,
		8: equals,
		9: setRelativeBase,
	}

	return Computer{program: program, input: input, memory: &memory, output: output, instructionSet: instructionSet}
}

// NOOP returns its input
func NOOP(x []int) []int {
	return x
}

// RunProgram runs a program, preprocessing it before executing.
func RunProgram(fileName string, input chan int, preprocess func([]int) []int) (out chan int) {
	program := preprocess(utils.ReadProgram(fileName))

	computer := NewComputer(&program, input)
	go computer.Execute()
	return computer.GetOutput()
}

// Execute is a routine to execute a program until it halts
func (c *Computer) Execute() {
	for {
		c.instruction = c.read(1)
		opcode := c.instruction % 100
		if opcode == 99 {
			break
		}
		fun := c.instructionSet[opcode]
		fun(c)
	}
	close(c.output)
}

func add(c *Computer) {
	x := c.read((c.instruction / 100) % 10)
	y := c.read((c.instruction / 1000) % 10)

	c.write(x+y, c.instruction/10000%10)
}

func multiply(c *Computer) {
	x := c.read((c.instruction / 100) % 10)
	y := c.read((c.instruction / 1000) % 10)

	c.write(x*y, c.instruction/10000%10)
}

func readInput(c *Computer) {
	res := <-c.input
	c.write(res, c.instruction/100%10)
}

func writeOutput(c *Computer) {
	out := c.read(c.instruction / 100 % 10)
	c.output <- out
}

func jumpIfTrue(c *Computer) {
	test := c.read(c.instruction / 100 % 10)
	newPos := c.read(c.instruction / 1000 % 10)
	if test != 0 {
		c.pointer = newPos
	}
}

func jumpIfFalse(c *Computer) {
	test := c.read(c.instruction / 100 % 10)
	newPos := c.read(c.instruction / 1000 % 10)
	if test == 0 {
		c.pointer = newPos
	}
}

func lessThan(c *Computer) {
	x := c.read(c.instruction / 100 % 10)
	y := c.read(c.instruction / 1000 % 10)
	if x < y {
		c.write(1, c.instruction/10000%10)
	} else {
		c.write(0, c.instruction/10000%10)
	}
}

func equals(c *Computer) {
	x := c.read(c.instruction / 100 % 10)
	y := c.read(c.instruction / 1000 % 10)
	if x == y {
		c.write(1, c.instruction/10000%10)
	} else {
		c.write(0, c.instruction/10000%10)
	}
}

func (c *Computer) readMemory(pos int) int {
	program := *c.program
	extraMemory := *c.memory
	if pos >= len(program) {
		return extraMemory[pos]
	}
	return program[pos]
}

func (c *Computer) writeMemory(pos int, value int) {
	program := *c.program
	extraMemory := *c.memory
	if pos >= len(program) {
		extraMemory[pos] = value
		return
	}
	program[pos] = value
}

func (c *Computer) read(mode int) int {
	var address int
	switch mode {
	case 0:
		address = c.readMemory(c.pointer)
	case 1:
		address = c.pointer
	case 2:
		address = c.readMemory(c.pointer) + c.relativeBase
	}
	c.pointer++
	return c.readMemory(address)
}

func (c *Computer) write(value int, mode int) int {
	var address int
	switch mode {
	case 0:
		address = c.readMemory(c.pointer)
	case 1:
		address = c.pointer
	case 2:
		address = c.readMemory(c.pointer) + c.relativeBase
	}
	c.writeMemory(address, value)

	c.pointer++
	return address
}

// GetOutput exposes the output channel for this computer
func (c *Computer) GetOutput() chan int {
	return c.output
}

func setRelativeBase(c *Computer) {
	x := c.read(c.instruction / 100 % 10)
	c.relativeBase += x
}
