package utils

type Computer struct {
	program      *[]int
	memory       *map[int]int
	input        int
	output       int
	pointer      int
	instruction  int
	relativeBase int
}

func NewComputer(program *[]int, input int) Computer {
	memory := make(map[int]int)
	return Computer{program: program, input: input, memory: &memory}
}

func (c *Computer) Execute() (output int, code string) {
	c.instruction = c.read(1)
	opcode := c.instruction % 100
	switch opcode {
	case 99:
		return c.output, "HALT"
	case 1:
		return c.add(), "OP"
	case 2:
		return c.multiply(), "OP"
	case 3:
		return c.readInput(), "OP"
	case 4:
		return c.writeOutput(), "OUTPUT"
	case 5:
		return c.jumpIfTrue(), "OP"
	case 6:
		return c.jumpIfFalse(), "OP"
	case 7:
		return c.lessThan(), "OP"
	case 8:
		return c.equals(), "OP"
	case 9:
		return c.setRelativeBase(), "OP"
	}
	return c.output, "ERROR"
}

func (c *Computer) add() int {
	x := c.read((c.instruction / 100) % 10)
	y := c.read((c.instruction / 1000) % 10)

	c.write(x+y, c.instruction/10000%10)
	// fmt.Printf("Add %d + %d = %d@%d\n", x, y, x+y, pos)
	return c.output
}

func (c *Computer) multiply() int {
	x := c.read((c.instruction / 100) % 10)
	y := c.read((c.instruction / 1000) % 10)

	c.write(x*y, c.instruction/10000%10)
	// fmt.Printf("Multiply %d * %d = %d@%d\n", x, y, x*y, pos)
	return c.output
}

func (c *Computer) readInput() int {
	c.write(c.input, c.instruction/100%10)
	// fmt.Printf("Set %d to input %d\n", pos, c.input)
	return c.output
}

func (c *Computer) writeOutput() int {
	c.output = c.read(c.instruction / 100 % 10)
	// fmt.Printf("Read output %d\n", c.output)
	// c.pointer++
	return c.output
}

func (c *Computer) jumpIfTrue() int {
	test := c.read(c.instruction / 100 % 10)
	newPos := c.read(c.instruction / 1000 % 10)
	// fmt.Printf("Test %d != 0?", test)
	if test != 0 {
		// fmt.Printf(" Yes! move pointer from %d to %d", c.pointer, newPos)
		c.pointer = newPos
	}
	// fmt.Println()
	return c.output
}

func (c *Computer) jumpIfFalse() int {
	test := c.read(c.instruction / 100 % 10)
	newPos := c.read(c.instruction / 1000 % 10)
	// fmt.Printf("Test %d == 0?", test)
	if test == 0 {
		// fmt.Printf(" Yes! move pointer from %d to %d", c.pointer, newPos)
		c.pointer = newPos
	}
	// fmt.Println()
	return c.output
}

func (c *Computer) lessThan() int {
	x := c.read(c.instruction / 100 % 10)
	y := c.read(c.instruction / 1000 % 10)
	// fmt.Printf("Test %d < %d?", x, y)
	if x < y {
		c.write(1, c.instruction/10000%10)
		// fmt.Printf(" Yes! write 1 to %d\n", pos)
	} else {
		c.write(0, c.instruction/10000%10)
		// fmt.Printf(" No! write 0 to %d\n", pos)
	}
	return c.output
}

func (c *Computer) equals() int {
	x := c.read(c.instruction / 100 % 10)
	y := c.read(c.instruction / 1000 % 10)
	// fmt.Printf("Test %d == %d?", x, y)
	if x == y {
		c.write(1, c.instruction/10000%10)
		// fmt.Printf(" Yes! write 1 to %d\n", pos)
	} else {
		c.write(0, c.instruction/10000%10)
		// fmt.Printf(" No! write 0 to %d\n", pos)
	}
	return c.output
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

func (c *Computer) SetInput(input int) {
	c.input = input
}

func (c *Computer) GetOutput() int {
	return c.output
}

func (c *Computer) setRelativeBase() int {
	x := c.read(c.instruction / 100 % 10)
	c.relativeBase += x
	return c.output
}
