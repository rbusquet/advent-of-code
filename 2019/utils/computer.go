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
	// logger       *log.Logger
}

// NewComputer instantiates a new computer object
func NewComputer(program *[]int, input chan int) Computer {
	memory := make(map[int]int)
	output := make(chan int)
	// logger := log.New(os.Stdout, fmt.Sprintf("ID %.6s: ", uuid.New()), 0)
	return Computer{program: program, input: input, memory: &memory, output: output} // logger: logger}
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
	// c.logger.Println("Closing output...")
	close(c.output)
	return
}

func (c *Computer) add() {
	x := c.read((c.instruction / 100) % 10)
	y := c.read((c.instruction / 1000) % 10)

	c.write(x+y, c.instruction/10000%10)
	// c.logger.Printf("Add %d + %d = %d@%d\n", x, y, x+y, pos)
}

func (c *Computer) multiply() {
	x := c.read((c.instruction / 100) % 10)
	y := c.read((c.instruction / 1000) % 10)

	c.write(x*y, c.instruction/10000%10)
	// c.logger.Printf("Multiply %d * %d = %d@%d\n", x, y, x*y, pos)
}

func (c *Computer) readInput() {
	// c.logger.Println("Waiting for input...")
	res := <-c.input
	c.write(res, c.instruction/100%10)
	// c.logger.Printf("save %d @ %d\n", res, pos)
}

func (c *Computer) writeOutput() {
	out := c.read(c.instruction / 100 % 10)
	c.output <- out
	// c.logger.Printf("Set output %d\n", out)
	// c.pointer++
}

func (c *Computer) jumpIfTrue() {
	test := c.read(c.instruction / 100 % 10)
	newPos := c.read(c.instruction / 1000 % 10)
	// c.logger.Printf("Test %d != 0?", test)
	if test != 0 {
		// c.logger.Printf(" Yes! move pointer from %d to %d\n", c.pointer, newPos)
		c.pointer = newPos
	}
	// fmt.Println()
}

func (c *Computer) jumpIfFalse() {
	test := c.read(c.instruction / 100 % 10)
	newPos := c.read(c.instruction / 1000 % 10)
	// c.logger.Printf("Test %d == 0?", test)
	if test == 0 {
		// c.logger.Printf(" Yes! move pointer from %d to %d\n", c.pointer, newPos)
		c.pointer = newPos
	}
	// fmt.Println()
}

func (c *Computer) lessThan() {
	x := c.read(c.instruction / 100 % 10)
	y := c.read(c.instruction / 1000 % 10)
	// c.logger.Printf("Test %d < %d?", x, y)
	if x < y {
		c.write(1, c.instruction/10000%10)
		// c.logger.Printf(" Yes! write 1 to %d\n", pos)
	} else {
		c.write(0, c.instruction/10000%10)
		// c.logger.Printf(" No! write 0 to %d\n", pos)
	}
}

func (c *Computer) equals() {
	x := c.read(c.instruction / 100 % 10)
	y := c.read(c.instruction / 1000 % 10)
	// c.logger.Printf("Test %d == %d?", x, y)
	if x == y {
		c.write(1, c.instruction/10000%10)
		// c.logger.Printf(" Yes! write 1 to %d\n", pos)
	} else {
		c.write(0, c.instruction/10000%10)
		// c.logger.Printf(" No! write 0 to %d\n", pos)
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
