package main

import (
	"fmt"

	"github.com/rbusquet/advent-of-code/utils"
)

func main() {
	file, scanner := utils.GenerateCommaSeparatedScanner("./input.txt")
	defer file.Close()
	direction := 0
	visited := make(map[utils.Position]bool)
	x, y := 0, 0
	visited[utils.NewPosition(x, y)] = true
	answeredPartTwo := false
	for scanner.Scan() {
		var turn string
		var count int
		instruction := scanner.Text()
		// fmt.Println(instruction)
		_, err := fmt.Sscanf(instruction, "%1s%d", &turn, &count)
		if err != nil {
			panic(err)
		}
		switch turn {
		case "R":
			direction++
			if direction >= 4 {
				direction = 0
			}
		case "L":
			direction--
			if direction < 0 {
				direction = 3
			}
		}

		for index := 0; index < count; index++ {
			switch direction {
			case 0:
				y++
			case 1:
				x++
			case 2:
				y--
			case 3:
				x--
			}

			pos := utils.NewPosition(x, y)
			if visited[pos] && !answeredPartTwo {
				fmt.Println("Part two output:", utils.AbsInt(x)+utils.AbsInt(y))
				answeredPartTwo = true
			}
			visited[pos] = true
		}
	}

	fmt.Println("Part one output:", utils.AbsInt(x)+utils.AbsInt(y))
}
