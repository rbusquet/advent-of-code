package main

import (
	"bufio"
	"fmt"
	"os"
	"path/filepath"
	"strconv"
)

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

	lst := make(map[int]bool)
	for scanner.Scan() {
		x := scanner.Text()
		if number, err := strconv.Atoi(x); err == nil {
			lst[number] = true
		}
	}
	for number := range lst {
		if lst[2020-number] {
			fmt.Println(number * (2020 - number))
			return
		}
	}
}
