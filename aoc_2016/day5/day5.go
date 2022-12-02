package main

import (
	"crypto/md5"
	"fmt"
	"io"
	"strconv"
)

func part1() {
	input := "wtnhxymk"

	password := ""

	for index := 0; ; index++ {
		if len(password) == 8 {
			break
		}
		h := md5.New()
		io.WriteString(h, input)
		io.WriteString(h, strconv.Itoa(index))
		result := fmt.Sprintf("%x", h.Sum(nil))
		if result[:5] == "00000" {
			password += string(rune(result[5]))
			fmt.Print(".")
		}
	}
	fmt.Println(password)
}

func main() {
	input := "wtnhxymk"

	password := make([]string, 8)
	found := 0
	seen := make(map[rune]bool)
	for index := 0; ; index++ {
		if found == 8 {
			break
		}
		h := md5.New()
		io.WriteString(h, input)
		io.WriteString(h, strconv.Itoa(index))
		result := fmt.Sprintf("%x", h.Sum(nil))
		if result[:5] == "00000" {
			r := rune(result[5])
			if r > '7' || seen[r] {
				continue
			}
			seen[r] = true
			position, _ := strconv.Atoi(string(r))
			password[position] = string(rune(result[6]))
			found++
		}
	}
	fmt.Print(password)
}
