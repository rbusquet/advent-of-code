package main

import (
	"fmt"

	"github.com/rbusquet/advent-of-code/utils"
)

func part1() {
	file, scanner := utils.GenerateLineScanner("./input.txt")
	defer file.Close()

	x, y := 0, 0
	keypad := map[utils.Position]int{
		utils.NewPosition(-1, 1):  1,
		utils.NewPosition(0, 1):   2,
		utils.NewPosition(1, 1):   3,
		utils.NewPosition(-1, 0):  4,
		utils.NewPosition(0, 0):   5,
		utils.NewPosition(1, 0):   6,
		utils.NewPosition(-1, -1): 7,
		utils.NewPosition(0, -1):  8,
		utils.NewPosition(1, -1):  9,
	}
	for scanner.Scan() {
		for _, char := range scanner.Text() {
			switch char {
			case 'U':
				y++
			case 'D':
				y--
			case 'L':
				x--
			case 'R':
				x++
			}
			if x > 1 {
				x = 1
			} else if x < -1 {
				x = -1
			}
			if y > 1 {
				y = 1
			} else if y < -1 {
				y = -1
			}
		}
		fmt.Print(keypad[utils.NewPosition(x, y)])
	}
}

func part2() {
	file, scanner := utils.GenerateLineScanner("./input.txt")
	defer file.Close()

	x, y := -2, 0 // '5'
	keypad := map[utils.Position]string{
		utils.NewPosition(0, 2):   "1",
		utils.NewPosition(-1, 1):  "2",
		utils.NewPosition(0, 1):   "3",
		utils.NewPosition(1, 1):   "4",
		utils.NewPosition(-2, 0):  "5",
		utils.NewPosition(-1, 0):  "6",
		utils.NewPosition(0, 0):   "7",
		utils.NewPosition(1, 0):   "8",
		utils.NewPosition(2, 0):   "9",
		utils.NewPosition(-1, -1): "A",
		utils.NewPosition(0, -1):  "B",
		utils.NewPosition(1, -1):  "C",
		utils.NewPosition(0, -2):  "D",
	}
	for scanner.Scan() {
		for _, char := range scanner.Text() {
			newX, newY := x, y
			switch char {
			case 'U':
				newY++
			case 'D':
				newY--
			case 'L':
				newX--
			case 'R':
				newX++
			}
			if _, exists := keypad[utils.NewPosition(newX, newY)]; exists {
				x, y = newX, newY
			}
		}
		fmt.Print(keypad[utils.NewPosition(x, y)])
	}
}

func main() {
	part1()
	part2()
}
