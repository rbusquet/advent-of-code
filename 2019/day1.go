package main

import "io/ioutil"

func calculateFuel(mass int) int {
	return mass/3 - 2
}

func main() {
	dat, err := ioutil.ReadFile("input1.txt")
	if err != nil {
		panic(err)
	}
}
