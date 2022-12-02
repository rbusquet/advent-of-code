package day4

import (
	"fmt"
	"regexp"
	"strconv"
	"strings"
)

func findPasswords(min int, max int) []string {
	passwords := []string{}
	for pwd := min; pwd <= max; pwd++ {
		s := strconv.Itoa(pwd)
		strPwd := strings.Split(s, "")
		foundDup := false
		decreasing := true
		lastDigit := strPwd[0]
		for _, digit := range strPwd[1:] {
			if lastDigit == digit {
				foundDup = true
			} else if digit < lastDigit {
				decreasing = false
			}
			lastDigit = digit
		}
		if foundDup && decreasing {
			passwords = append(passwords, s)
		}
	}
	return passwords
}

// Run day 4
func Run() {
	fmt.Println("-- Day 4 --")
	validPasswords := findPasswords(372037, 905157)
	fmt.Println("Part one output:", len(validPasswords))

	reg := regexp.MustCompile(`00+|11+|22+|33+|44+|55+|66+|77+|88+|99+`)

	count := 0
	for _, pwd := range validPasswords {
		matches := reg.FindAllString(pwd, -1)
		ok := false
		for _, match := range matches {
			if len(match) == 2 {
				ok = true
			}
		}
		if ok {
			count++
		}
	}
	fmt.Println("Part two output:", count)
}
