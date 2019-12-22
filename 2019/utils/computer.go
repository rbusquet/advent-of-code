package utils

// Computer can run programs using IntCode defined in adventofcode.com/2019
type Computer struct {
	program      *[]int
	memory       *map[int]int
	input        chan int
	output       chan int
	pointer      int
	instruction  int
	relativeBase int
}

// NewComputer instantiates a new computer object
func NewComputer(program *[]int, input chan int) Computer {
	memory := make(map[int]int)
	output := make(chan int)
	return Computer{program: program, input: input, memory: &memory, output: output}
}

// RunProgram runs a program, preprocessing it before executing.
func RunProgram(fileName string, input chan int, preprocess func([]int) []int) (out chan int) {
	program := preprocess(ReadProgram(fileName))

	computer := NewComputer(&program, input)
	go computer.Execute()
	return computer.GetOutput()
}

// Execute is a routine to execute a program until it halts
func (c *Computer) Execute() {
loop:
	for {
		c.instruction = c.read(1)
		opcode := c.instruction % 100
		switch opcode {
		case 99:
			break loop
		case 1:
			c.add()
		case 2:
			c.multiply()
		case 3:
			c.readInput()
		case 4:
			c.writeOutput()
		case 5:
			c.jumpIfTrue()
		case 6:
			c.jumpIfFalse()
		case 7:
			c.lessThan()
		case 8:
			c.equals()
		case 9:
			c.setRelativeBase()
		}
	}
	close(c.output)
	return
}

func (c *Computer) add() {
	x := c.read((c.instruction / 100) % 10)
	y := c.read((c.instruction / 1000) % 10)

	c.write(x+y, c.instruction/10000%10)
}

func (c *Computer) multiply() {
	x := c.read((c.instruction / 100) % 10)
	y := c.read((c.instruction / 1000) % 10)

	c.write(x*y, c.instruction/10000%10)
}

func (c *Computer) readInput() {
	res := <-c.input
	c.write(res, c.instruction/100%10)
}

func (c *Computer) writeOutput() {
	out := c.read(c.instruction / 100 % 10)
	c.output <- out
}

func (c *Computer) jumpIfTrue() {
	test := c.read(c.instruction / 100 % 10)
	newPos := c.read(c.instruction / 1000 % 10)
	if test != 0 {
		c.pointer = newPos
	}
}

func (c *Computer) jumpIfFalse() {
	test := c.read(c.instruction / 100 % 10)
	newPos := c.read(c.instruction / 1000 % 10)
	if test == 0 {
		c.pointer = newPos
	}
}

func (c *Computer) lessThan() {
	x := c.read(c.instruction / 100 % 10)
	y := c.read(c.instruction / 1000 % 10)
	if x < y {
		c.write(1, c.instruction/10000%10)
	} else {
		c.write(0, c.instruction/10000%10)
	}
}

func (c *Computer) equals() {
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

func (c *Computer) setRelativeBase() {
	x := c.read(c.instruction / 100 % 10)
	c.relativeBase += x
}
