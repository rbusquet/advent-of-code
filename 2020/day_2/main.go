package main

import (
	"bufio"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strconv"
)

func atoi(s string) int {
	if val, err := strconv.Atoi(s); err != nil {
		panic(err)
	} else {
		return val
	}
}

func part1(passwords []string) int {
	valid := 0
	exp := regexp.MustCompile(`(\d+)-(\d+) (.): (.*)`)

	for _, password := range passwords {
		match := exp.FindStringSubmatch(password)

		min := atoi(match[1])
		max := atoi(match[2])
		letter := match[3]
		password := match[4]

		counter := make(map[rune]int)
		for _, v := range password {
			counter[v]++
		}
		count := counter[rune(letter[0])]
		if count >= min && count <= max {
			valid++
		}
	}
	return valid
}

func part2(passwords []string) int {
	valid := 0
	exp := regexp.MustCompile(`(\d+)-(\d+) (.): (.*)`)

	for _, password := range passwords {
		match := exp.FindStringSubmatch(password)

		pos1 := atoi(match[1])
		pos2 := atoi(match[2])
		letter := match[3]
		password := match[4]

		a := password[pos1-1]
		b := password[pos2-2]
		letterMatch := letter[0] == a || letter[0] == b
		if letterMatch && a != b {
			valid++
		}
	}
	return valid
}

func generateLineScanner(fileName string) (*os.File, *bufio.Scanner) {
	if path, err := filepath.Abs(fileName); err != nil {
		panic(err)
	} else {
		if file, err := os.Open(path); err != nil {
			panic(err)
		} else {
			scanner := bufio.NewScanner(file)
			return file, scanner
		}
	}
}

func main() {
	file, scanner := generateLineScanner("./input.txt")
	defer file.Close()
	lst := make([]string, 0)
	for scanner.Scan() {
		lst = append(lst, scanner.Text())
	}
	fmt.Println(part1(lst))
	fmt.Println(part2(lst))
}
