package main

import (
	"fmt"

	"github.com/rbusquet/advent-of-code/utils"
)

func createRect(screen map[utils.Position]string, x, y int) map[utils.Position]string {
	for row := 0; row < y; row++ {
		for column := 0; column < x; column++ {
			screen[utils.NewPosition(column, row)] = "#"
		}
	}

	return screen
}

func rotateRow(screen map[utils.Position]string, row, count int) map[utils.Position]string {
	newRow := make([]string, 50)
	for pixel := 0; pixel < 50; pixel++ {
		atScreen := screen[utils.NewPosition(pixel, row)]
		destPixel := (pixel + count) % 50
		newRow[destPixel] = atScreen
	}
	for index := range newRow {
		screen[utils.NewPosition(index, row)] = newRow[index]
	}

	return screen
}

func rotateColumn(screen map[utils.Position]string, column, count int) map[utils.Position]string {
	newColumn := make([]string, 6)
	for pixel := 0; pixel < 6; pixel++ {
		atScreen := screen[utils.NewPosition(column, pixel)]
		destPixel := (pixel + count) % 6
		newColumn[destPixel] = atScreen
	}
	for index := range newColumn {
		screen[utils.NewPosition(column, index)] = newColumn[index]
	}

	return screen
}

func main() {
	screen := make(map[utils.Position]string)
	file, scanner := utils.GenerateLineScanner("./input.txt")
	defer file.Close()

	for scanner.Scan() {
		instruction := scanner.Text()
		var x, y int
		_, err := fmt.Sscanf(instruction, "rect %dx%d", &x, &y)
		if err == nil {
			screen = createRect(screen, x, y)
			continue
		}
		_, err = fmt.Sscanf(instruction, "rotate row y=%d by %d", &x, &y)
		if err == nil {
			screen = rotateRow(screen, x, y)
			continue
		}
		_, err = fmt.Sscanf(instruction, "rotate column x=%d by %d", &x, &y)
		if err == nil {
			screen = rotateColumn(screen, x, y)
			continue
		}
	}
	count := 0
	for row := 0; row < 6; row++ {
		for column := 0; column < 50; column++ {
			pixel := screen[utils.NewPosition(column, row)]
			if pixel == "" {
				pixel = " "
			} else if pixel == "#" {
				count++
			}
			fmt.Print(pixel)
		}
		fmt.Println()
	}
	fmt.Println(count)
}
