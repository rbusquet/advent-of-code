package main

import (
	"fmt"
	"regexp"
	"sort"
	"strconv"
	"strings"

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

	exp := regexp.MustCompile(`([a-z-]+)(\d+)\[([a-z]+)\]`)
	count := 0
loop:
	for scanner.Scan() {
		room := scanner.Text()
		matches := exp.FindStringSubmatch(room)

		counts := make(map[rune]int)

		room, sectorID, checksum := matches[1], matches[2], matches[3]

		for _, char := range room {
			if char == '-' {
				continue
			}
			counts[char]++
		}
		top := make(letterList, 0)
		for letter, count := range counts {
			top = append(top, letterCount{string(letter), count})
		}
		sort.Sort(top)
		for index := 0; index < 5; index++ {
			if !strings.Contains(checksum, top[index].letter) {
				continue loop
			}
		}
		sector, _ := strconv.Atoi(sectorID)
		count += sector

		actualName := ""
		for _, char := range room {
			if char == '-' {
				actualName += " "
				continue
			}
			position := int(char - 'a')
			decrypted := (position + sector) % 26
			actualName += string('a' + decrypted)
		}
		if strings.TrimSpace(actualName) == "northpole object storage" {
			fmt.Println("Part two output:", sector)
		}
	}
	fmt.Println("Part one output:", count)
}
