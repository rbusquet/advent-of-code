package day22

import (
	"fmt"
	"strings"

	"github.com/rbusquet/advent-of-code/utils"
)

func cut(deck []int, n int) []int {
	if n > 0 {
		return append(deck[n:], deck[:n]...)
	}
	return append(deck[len(deck)+n:], deck[:len(deck)+n]...)
}

func newStack(deck []int) []int {
	for i := len(deck)/2 - 1; i >= 0; i-- {
		opp := len(deck) - 1 - i
		deck[i], deck[opp] = deck[opp], deck[i]
	}
	return deck
}

func dealWithIncrement(deck []int, n int) []int {
	size := len(deck)
	newDeck := make([]int, size)

	for index, card := range deck {
		newIndex := index * n
		newDeck[newIndex%size] = card
	}
	return newDeck
}

func part1() {
	file, scanner := utils.GenerateLineScanner("./input.txt")
	defer file.Close()

	SIZE := 10007

	deck := make([]int, SIZE)
	for index := 0; index < SIZE; index++ {
		deck[index] = index
	}
	for scanner.Scan() {
		instruction := scanner.Text()
		fmt.Println(deck[2019])
		fmt.Println(instruction)
		var input int
		_, err := fmt.Sscanf(instruction, "cut %d", &input)
		if err == nil {
			deck = cut(deck, input)
			continue
		}
		if strings.TrimSpace(instruction) == "deal into new stack" {
			deck = newStack(deck)
			continue
		}
		_, err = fmt.Sscanf(instruction, "deal with increment %d", &input)
		if err == nil {
			deck = dealWithIncrement(deck, input)
			continue
		}
		panic("Oh oh")
	}
	fmt.Println(deck[2019])
}

// Run day22
func Run() {
	fmt.Println("-- Day 22 --")
	fmt.Print("Part one output: ")
	part1()
}
