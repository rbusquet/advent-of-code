package main

import (
	"fmt"
)

func main() {
	fmt.Println(memoryGame([]int{14, 3, 1, 0, 9, 5}, 2020))
	fmt.Println(memoryGame([]int{14, 3, 1, 0, 9, 5}, 30000000))
}

func memoryGame(input []int, stop int) (lastSpoken int) {
	seen := make(map[int]int)
	for index, value := range input {
		seen[value] = index
		lastSpoken = value
	}
	for index := len(input) - 1; index < stop-1; index++ {
		lastIndex, ok := seen[lastSpoken]
		if !ok {
			lastIndex = index
		}
		nextSpoken := index - lastIndex
		seen[lastSpoken] = index
		lastSpoken = nextSpoken
	}
	return lastSpoken
}
