package day14

import (
	"advent-of-code/2019/utils"
	"fmt"
	"strings"
)

// Parcel is an ingredient of a reaction
type Parcel struct {
	quantity int
	name     string
}

func part1() {
	reactions := make(map[string][]Parcel)
	units := make(map[string]int)

	scanner := utils.GenerateLineScanner("./day14/input.txt")
	for scanner.Scan() {
		reaction := strings.Split(scanner.Text(), " => ")
		var quantity int
		var name, parcelName string
		_, err := fmt.Sscanf(reaction[1], "%d %s", &quantity, &name)
		if err != nil {
			panic(err)
		}
		parcels := []Parcel{}
		units[name] = quantity

		for _, parcel := range strings.Split(reaction[0], ", ") {
			_, err := fmt.Sscanf(parcel, "%d %s", &quantity, &parcelName)
			if err != nil {
				panic(err)
			}
			p := Parcel{quantity, parcelName}
			parcels = append(parcels, p)
		}
		reactions[name] = parcels
	}
	var calc func(int, string)
	amounts := make(map[string]int)
	oreNeeded := 0
	calc = func(toCreate int, chem string) {
		if chem == "ORE" {
			oreNeeded += toCreate
			return
		}
		if _, exists := amounts[chem]; !exists {
			amounts[chem] = 0
		}
		current := amounts[chem]
		resultUnits := units[chem]
		recipe := reactions[chem]

		produced := 0
		for produced+current < toCreate {
			for _, parcel := range recipe {
				need := parcel.quantity
				parcelChem := parcel.name
				calc(need, parcelChem)
			}
			produced += resultUnits
		}

		amounts[chem] += produced - toCreate
	}
	calc(1, "FUEL")
	fmt.Println(oreNeeded)
}

func part2() {
	reactions := make(map[string][]Parcel)
	units := make(map[string]int)

	scanner := utils.GenerateLineScanner("./day14/input.txt")
	for scanner.Scan() {
		reaction := strings.Split(scanner.Text(), " => ")
		var quantity int
		var name, parcelName string
		_, err := fmt.Sscanf(reaction[1], "%d %s", &quantity, &name)
		if err != nil {
			panic(err)
		}
		parcels := []Parcel{}
		units[name] = quantity

		for _, parcel := range strings.Split(reaction[0], ", ") {
			_, err := fmt.Sscanf(parcel, "%d %s", &quantity, &parcelName)
			if err != nil {
				panic(err)
			}
			p := Parcel{quantity, parcelName}
			parcels = append(parcels, p)
		}
		reactions[name] = parcels
	}
	var calc func(int, string)
	amounts := make(map[string]int)
	oreNeeded := 0
	calc = func(toCreate int, chem string) {
		if chem == "ORE" {
			oreNeeded += toCreate
			return
		}
		if _, exists := amounts[chem]; !exists {
			amounts[chem] = 0
		}
		current := amounts[chem]
		resultUnits := units[chem]
		recipe := reactions[chem]

		multiplier := 1
		if resultUnits < toCreate {
			multiplier = toCreate / resultUnits
			if toCreate%resultUnits > 0 {
				multiplier++
			}
		}

		produced := 0
		for produced+current < toCreate {
			for _, parcel := range recipe {
				need := multiplier * parcel.quantity
				parcelChem := parcel.name
				calc(need, parcelChem)
			}
			produced += resultUnits * multiplier
		}

		amounts[chem] += produced - toCreate
	}
	totalFuel := 0
	// try with high fuel amount
	maxTotalFuel := 1000000000000
	minTotalFuel := 0
	for {
		totalFuel = (maxTotalFuel + minTotalFuel) / 2
		calc(totalFuel, "FUEL")
		if oreNeeded > 1000000000000 {
			maxTotalFuel = totalFuel
		} else if oreNeeded < 1000000000000 {
			minTotalFuel = totalFuel
		}
		oreNeeded = 0
		amounts = make(map[string]int)
		if maxTotalFuel-minTotalFuel <= 1 {
			totalFuel = maxTotalFuel
			break
		}
	}
	calc(totalFuel, "FUEL")
	for oreNeeded > 1000000000000 {
		oreNeeded = 0
		amounts = make(map[string]int)
		totalFuel--
		calc(totalFuel, "FUEL")
	}
	fmt.Println(totalFuel + 1) // I don't know why :(
}

// Run day 14
func Run() {
	fmt.Println("-- Day 14 --")
	fmt.Print("Part one output: ")
	part1()
	fmt.Print("Part two output: ")
	part2()
}
