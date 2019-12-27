package main

import (
	"bufio"
	"fmt"

	"github.com/rbusquet/advent-of-code/utils"
)

func possible(x, y, z int) bool {
	a := x+y > z
	b := x+z > y
	c := y+z > x
	return a && b && c
}

func part1() {
	file, scanner := utils.GenerateLineScanner("./input.txt")
	defer file.Close()
	count := 0
	for scanner.Scan() {
		var x, y, z int
		triangle := scanner.Text()
		_, err := fmt.Sscanf(triangle, "%d %d %d", &x, &y, &z)
		if err != nil {
			panic(err)
		}

		if possible(x, y, z) {
			count++
		}
	}
	fmt.Println(count)
}

func read(scanner *bufio.Scanner) (int, int, int) {
	var x, y, z int
	triangle := scanner.Text()
	_, err := fmt.Sscanf(triangle, "%d %d %d", &x, &y, &z)
	if err != nil {
		panic(err)
	}
	return x, y, z
}

func main() {
	file, scanner := utils.GenerateLineScanner("./input.txt")
	defer file.Close()
	count := 0
	for {
		cont := scanner.Scan()
		if !cont {
			break
		}
		x1, x2, x3 := read(scanner)
		scanner.Scan()
		y1, y2, y3 := read(scanner)
		scanner.Scan()
		z1, z2, z3 := read(scanner)
		if possible(x1, y1, z1) {
			count++
		}
		if possible(x2, y2, z2) {
			count++
		}
		if possible(x3, y3, z3) {
			count++
		}
	}
	fmt.Println(count)
}
