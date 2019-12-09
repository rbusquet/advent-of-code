package utils

type Computer struct {
	program     *[]int
	input       int
	output      int
	pointer     int
	instruction int
}

func NewComputer(program *[]int, input int) Computer {
	return Computer{program: program, input: input}
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
	}
	return c.output, "ERROR"
}

func (c *Computer) add() int {
	x := c.read((c.instruction / 100) % 10)
	y := c.read((c.instruction / 1000) % 10)

	c.write(x + y)
	// fmt.Printf("Add %d + %d = %d@%d\n", x, y, x+y, pos)
	return c.output
}

func (c *Computer) multiply() int {
	x := c.read((c.instruction / 100) % 10)
	y := c.read((c.instruction / 1000) % 10)

	c.write(x * y)
	// fmt.Printf("Multiply %d * %d = %d@%d\n", x, y, x*y, pos)
	return c.output
}

func (c *Computer) readInput() int {
	c.write(c.input)
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
		c.write(1)
		// fmt.Printf(" Yes! write 1 to %d\n", pos)
	} else {
		c.write(0)
		// fmt.Printf(" No! write 0 to %d\n", pos)
	}
	return c.output
}

func (c *Computer) equals() int {
	x := c.read(c.instruction / 100 % 10)
	y := c.read(c.instruction / 1000 % 10)
	// fmt.Printf("Test %d == %d?", x, y)
	if x == y {
		c.write(1)
		// fmt.Printf(" Yes! write 1 to %d\n", pos)
	} else {
		c.write(0)
		// fmt.Printf(" No! write 0 to %d\n", pos)
	}
	return c.output
}

func (c *Computer) read(mode int) int {
	memory := *c.program
	var value int
	switch mode {
	case 0:
		value = memory[memory[c.pointer]]
	case 1:
		value = memory[c.pointer]
	}
	c.pointer++
	return value
}

func (c *Computer) write(value int) int {
	pos := (*c.program)[c.pointer]
	(*c.program)[pos] = value
	c.pointer++
	return pos
}

func (c *Computer) SetInput(input int) {
	c.input = input
}

func (c *Computer) GetOutput() int {
	return c.output
}
