package main

import (
	"errors"
	"fmt"
)

// Computer computes
type Computer struct {
	program     *[]int
	input       int
	output      int
	pointer     int
	instruction int
}

func (c *Computer) nextInstruction() error {
	c.instruction = c.read(1)
	opcode := c.instruction % 100
	switch opcode {
	case 99:
		return errors.New("HALT")
	case 1:
		return c.add()
	case 2:
		return c.multiply()
	case 3:
		return c.readInput()
	case 4:
		return c.writeOutput()
	case 5:
		return c.jumpIfTrue()
	case 6:
		return c.jumpIfFalse()
	case 7:
		return c.lessThan()
	case 8:
		return c.equals()
	}
	return errors.New("Unkown opcode")
}

func (c *Computer) add() error {
	x := c.read((c.instruction / 100) % 10)
	y := c.read((c.instruction / 1000) % 10)

	pos := c.write(x + y)
	fmt.Printf("Add %d + %d = %d@%d\n", x, y, x+y, pos)
	return nil
}

func (c *Computer) multiply() error {
	x := c.read((c.instruction / 100) % 10)
	y := c.read((c.instruction / 1000) % 10)

	pos := c.write(x * y)
	fmt.Printf("Multiply %d * %d = %d@%d\n", x, y, x*y, pos)
	return nil
}

func (c *Computer) readInput() error {
	pos := c.write(c.input)
	fmt.Printf("Set %d to input %d\n", pos, c.input)
	return nil
}

func (c *Computer) writeOutput() error {
	c.output = c.read(c.instruction / 100 % 10)
	fmt.Printf("Read output %d\n", c.output)
	// c.pointer++
	return nil
}

func (c *Computer) jumpIfTrue() error {
	test := c.read(c.instruction / 100 % 10)
	newPos := c.read(c.instruction / 1000 % 10)
	fmt.Printf("Test %d != 0?", test)
	if test != 0 {
		fmt.Printf(" Yes! move pointer from %d to %d", c.pointer, newPos)
		c.pointer = newPos
	}
	fmt.Println()
	return nil
}

func (c *Computer) jumpIfFalse() error {
	test := c.read(c.instruction / 100 % 10)
	newPos := c.read(c.instruction / 1000 % 10)
	fmt.Printf("Test %d == 0?", test)
	if test == 0 {
		fmt.Printf(" Yes! move pointer from %d to %d", c.pointer, newPos)
		c.pointer = newPos
	}
	fmt.Println()
	return nil
}

func (c *Computer) lessThan() error {
	x := c.read(c.instruction / 100 % 10)
	y := c.read(c.instruction / 1000 % 10)
	fmt.Printf("Test %d < %d?", x, y)
	if x < y {
		pos := c.write(1)
		fmt.Printf(" Yes! write 1 to %d\n", pos)
	} else {
		pos := c.write(0)
		fmt.Printf(" No! write 0 to %d\n", pos)
	}
	return nil
}

func (c *Computer) equals() error {
	x := c.read(c.instruction / 100 % 10)
	y := c.read(c.instruction / 1000 % 10)
	fmt.Printf("Test %d == %d?", x, y)
	if x == y {
		pos := c.write(1)
		fmt.Printf(" Yes! write 1 to %d\n", pos)
	} else {
		pos := c.write(0)
		fmt.Printf(" No! write 0 to %d\n", pos)
	}
	return nil
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

func main() {
	memory := []int{3, 225, 1, 225, 6, 6, 1100, 1, 238, 225, 104, 0, 1101, 37, 61, 225, 101, 34, 121, 224, 1001, 224, -49, 224, 4, 224, 102, 8, 223, 223, 1001, 224, 6, 224, 1, 224, 223, 223, 1101, 67, 29, 225, 1, 14, 65, 224, 101, -124, 224, 224, 4, 224, 1002, 223, 8, 223, 101, 5, 224, 224, 1, 224, 223, 223, 1102, 63, 20, 225, 1102, 27, 15, 225, 1102, 18, 79, 224, 101, -1422, 224, 224, 4, 224, 102, 8, 223, 223, 1001, 224, 1, 224, 1, 223, 224, 223, 1102, 20, 44, 225, 1001, 69, 5, 224, 101, -32, 224, 224, 4, 224, 1002, 223, 8, 223, 101, 1, 224, 224, 1, 223, 224, 223, 1102, 15, 10, 225, 1101, 6, 70, 225, 102, 86, 40, 224, 101, -2494, 224, 224, 4, 224, 1002, 223, 8, 223, 101, 6, 224, 224, 1, 223, 224, 223, 1102, 25, 15, 225, 1101, 40, 67, 224, 1001, 224, -107, 224, 4, 224, 102, 8, 223, 223, 101, 1, 224, 224, 1, 223, 224, 223, 2, 126, 95, 224, 101, -1400, 224, 224, 4, 224, 1002, 223, 8, 223, 1001, 224, 3, 224, 1, 223, 224, 223, 1002, 151, 84, 224, 101, -2100, 224, 224, 4, 224, 102, 8, 223, 223, 101, 6, 224, 224, 1, 224, 223, 223, 4, 223, 99, 0, 0, 0, 677, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1105, 0, 99999, 1105, 227, 247, 1105, 1, 99999, 1005, 227, 99999, 1005, 0, 256, 1105, 1, 99999, 1106, 227, 99999, 1106, 0, 265, 1105, 1, 99999, 1006, 0, 99999, 1006, 227, 274, 1105, 1, 99999, 1105, 1, 280, 1105, 1, 99999, 1, 225, 225, 225, 1101, 294, 0, 0, 105, 1, 0, 1105, 1, 99999, 1106, 0, 300, 1105, 1, 99999, 1, 225, 225, 225, 1101, 314, 0, 0, 106, 0, 0, 1105, 1, 99999, 108, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 329, 101, 1, 223, 223, 1107, 677, 226, 224, 102, 2, 223, 223, 1006, 224, 344, 101, 1, 223, 223, 8, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 359, 101, 1, 223, 223, 1008, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 374, 101, 1, 223, 223, 7, 226, 677, 224, 1002, 223, 2, 223, 1006, 224, 389, 1001, 223, 1, 223, 1007, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 404, 1001, 223, 1, 223, 7, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 419, 1001, 223, 1, 223, 1008, 677, 226, 224, 1002, 223, 2, 223, 1005, 224, 434, 1001, 223, 1, 223, 1107, 226, 677, 224, 102, 2, 223, 223, 1005, 224, 449, 1001, 223, 1, 223, 1008, 226, 226, 224, 1002, 223, 2, 223, 1006, 224, 464, 1001, 223, 1, 223, 1108, 677, 677, 224, 102, 2, 223, 223, 1006, 224, 479, 101, 1, 223, 223, 1108, 226, 677, 224, 1002, 223, 2, 223, 1006, 224, 494, 1001, 223, 1, 223, 107, 226, 226, 224, 1002, 223, 2, 223, 1006, 224, 509, 1001, 223, 1, 223, 8, 226, 677, 224, 102, 2, 223, 223, 1006, 224, 524, 1001, 223, 1, 223, 1007, 226, 226, 224, 1002, 223, 2, 223, 1006, 224, 539, 1001, 223, 1, 223, 107, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 554, 1001, 223, 1, 223, 1107, 226, 226, 224, 102, 2, 223, 223, 1005, 224, 569, 101, 1, 223, 223, 1108, 677, 226, 224, 1002, 223, 2, 223, 1006, 224, 584, 1001, 223, 1, 223, 1007, 677, 226, 224, 1002, 223, 2, 223, 1005, 224, 599, 101, 1, 223, 223, 107, 226, 677, 224, 102, 2, 223, 223, 1005, 224, 614, 1001, 223, 1, 223, 108, 226, 226, 224, 1002, 223, 2, 223, 1005, 224, 629, 101, 1, 223, 223, 7, 677, 226, 224, 102, 2, 223, 223, 1005, 224, 644, 101, 1, 223, 223, 8, 677, 226, 224, 102, 2, 223, 223, 1006, 224, 659, 1001, 223, 1, 223, 108, 677, 226, 224, 102, 2, 223, 223, 1005, 224, 674, 1001, 223, 1, 223, 4, 223, 99, 226}

	computer := Computer{&memory, 5, 0, 0, -1}

	for {
		err := computer.nextInstruction()
		if err != nil {
			fmt.Println(err)
			break
		}
	}
}
