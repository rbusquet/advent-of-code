package day1

import (
	"fmt"
	"strconv"

	"github.com/rbusquet/advent-of-code/utils"
)

func calculateFuel(mass int) int {
	return mass/3 - 2
}

func calculateTotalFuel(mass int) int {
	if fuel := calculateFuel(mass); fuel >= 0 {
		return fuel + calculateTotalFuel(fuel)
	}
	return 0
}

// Run day 1
func Run() {
	fmt.Println("-- Day 1 --")
	file, scanner := utils.GenerateLineScanner("./2019/day1/input.txt")
	defer (*file).Close()
	total := 0

	totalWithFuel := 0
	for scanner.Scan() {
		if mass, err := strconv.Atoi(scanner.Text()); err != nil {
			panic(err)
		} else {
			total = total + calculateFuel(mass)
			totalWithFuel = totalWithFuel + calculateTotalFuel(mass)
		}
	}

	fmt.Println("Part one output:", total)
	fmt.Println("Part two output:", totalWithFuel)
}
