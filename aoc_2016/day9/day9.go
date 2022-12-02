package main

import (
	"fmt"

	"github.com/rbusquet/advent-of-code/utils"
)

// Bit holds compression information for data
type Bit struct {
	length, multiplier int
	bit                string
	children           []Bit
}

func (b *Bit) decompressedV1() int {
	return b.multiplier * b.length
}

func (b *Bit) decompressedV2() int {
	if len(b.children) == 0 {
		return b.decompressedV1()
	}
	total := 0
	for _, child := range b.children {
		total += b.multiplier * child.decompressedV2()
	}
	return total
}

func getBits(line string) []Bit {
	bits := []Bit{}
	if line[0] != '(' {
		return bits
	}
	for len(line) > 0 {
		var length, multiplier int
		var rest, bit string
		fmt.Sscanf(line, "(%dx%d)%s", &length, &multiplier, &rest)
		bit, line = rest[:length], rest[length:]
		children := getBits(bit)
		newBit := Bit{length, multiplier, bit, children}
		bits = append(bits, newBit)
	}
	return bits
}

func main() {
	file, scanner := utils.GenerateLineScanner("./input.txt")
	defer file.Close()
	scanner.Scan()
	line := scanner.Text()
	bits := getBits(line)
	v1 := 0
	v2 := 0
	for index := range bits {
		v1 += bits[index].decompressedV1()
		v2 += bits[index].decompressedV2()
	}
	fmt.Println(v1)
	fmt.Println(v2)
}
