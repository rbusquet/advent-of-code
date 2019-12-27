package main

import (
	"fmt"
	"regexp"

	"github.com/rbusquet/advent-of-code/utils"
)

func hasABBA(bit string) bool {
	size := len(bit)
	for index := range bit {
		if index >= size-3 {
			break
		}
		outerPal := bit[index] == bit[index+3]
		innerPal := bit[index+1] == bit[index+2]
		diffInner := bit[index] != bit[index+1]
		if outerPal && innerPal && diffInner {
			return true
		}
	}
	return false
}

func isTLS(address string) bool {
	splitter := regexp.MustCompile(`[\[\]]`)
	result := false
	for index, bit := range splitter.Split(address, -1) {
		if index%2 == 0 {
			result = result || hasABBA(bit)
		} else {
			if hasABBA(bit) {
				return false
			}
		}
	}
	return result
}

func findABA(bit string) []string {
	res := []string{}
	size := len(bit)
	for index := range bit {
		if index >= size-2 {
			break
		}
		outerPal := bit[index] == bit[index+2]
		diffInner := bit[index] != bit[index+1]
		if outerPal && diffInner {
			res = append(res, bit[index:index+2])
		}
	}
	return res
}

func hasBAB(bit string, babas []string) bool {
	size := len(bit)
	for index := range bit {
		if index >= size-2 {
			break
		}
		outerPal := bit[index] == bit[index+2]
		diffInner := bit[index] != bit[index+1]
		if !outerPal || !diffInner {
			continue
		}
		for _, bab := range babas {
			outerCheck := bit[index] == bab[1]
			innerCheck := bit[index+1] == bab[0]
			if outerCheck && innerCheck {
				return true
			}
		}
	}
	return false
}

func isSSL(address string) bool {
	splitter := regexp.MustCompile(`[\[\]]`)
	splitted := splitter.Split(address, -1)

	abas := []string{}
	for index, bit := range splitted {
		if index%2 == 0 {
			abas = append(abas, findABA(bit)...)
		}
	}
	for index, bit := range splitted {
		if index%2 != 0 {
			if hasBAB(bit, abas) {
				return true
			}
		}
	}
	return false
}

func main() {
	file, scanner := utils.GenerateLineScanner("./input.txt")
	defer file.Close()

	countTLS := 0
	countSSL := 0
	for scanner.Scan() {
		address := scanner.Text()
		if isTLS(address) {
			countTLS++
		}
		if isSSL(address) {
			countSSL++
		}
	}
	fmt.Println(countTLS)
	fmt.Println(countSSL)
}
