package main

import (
	"fmt"
	"sort"

	"github.com/rbusquet/advent-of-code/utils"
)

type letterCount struct {
	letter string
	count  int
}

type letterList []letterCount

func (a letterList) Len() int      { return len(a) }
func (a letterList) Swap(i, j int) { a[i], a[j] = a[j], a[i] }
func (a letterList) Less(i, j int) bool {
	if a[i].count == a[j].count {
		return a[i].letter < a[j].letter
	}
	return a[i].count > a[j].count
}

func main() {
	file, scanner := utils.GenerateLineScanner("./input.txt")
	defer file.Close()
	counts := make(map[int]map[rune]int, 8)
	for scanner.Scan() {
		for index, char := range scanner.Text() {
			if _, exists := counts[index]; !exists {
				counts[index] = make(map[rune]int)
			}
			counts[index][char]++
		}
	}
	wordPart1 := ""
	wordPart2 := ""
	for index := 0; index < 8; index++ {
		top := make(letterList, 0)
		for letter, count := range counts[index] {
			top = append(top, letterCount{string(letter), count})
		}
		sort.Sort(top)
		wordPart1 += top[0].letter
		wordPart2 += top[len(top)-1].letter
	}
	fmt.Println(wordPart1)
	fmt.Println(wordPart2)
}
