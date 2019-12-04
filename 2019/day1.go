package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func calculateFuel(mass int) int {
	return mass/3 - 2
}

func calculateTotalFuel(mass int) int {
	if fuel := calculateFuel(mass); fuel >= 0 {
		return fuel + calculateTotalFuel(fuel)
	}
	return 0
}

func main() {
	if dat, err := os.Open("input1.txt"); err != nil {
		panic(err)
	} else {
		scanner := bufio.NewScanner(dat)
		total := 0
		totalWithFuel := 0
		for scanner.Scan() {
			if mass, err := strconv.Atoi(scanner.Text()); err != nil {
				panic(err)
			} else {
				total = total + calculateFuel(mass)
				totalWithFuel = totalWithFuel + calculateTotalFuel(mass)
			}
		}
		fmt.Println("total", total)
		fmt.Println("total with fuel", totalWithFuel)
	}
}
