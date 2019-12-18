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

// State holds state from receipes, inventory
type State struct {
	amounts, units map[string]int
	reactions      map[string][]Parcel
}

func (s *State) getCost(toCreate int, chem string) int {
	if chem == "ORE" {
		return toCreate
	}
	current := s.amounts[chem]
	resultUnits := s.units[chem]
	recipe := s.reactions[chem]

	if current >= toCreate {
		s.amounts[chem] = current - toCreate
		return 0
	}
	s.amounts[chem] = 0
	toCreate -= current
	current = 0

	multiplier := 1
	if resultUnits < toCreate {
		multiplier = toCreate / resultUnits
		if toCreate%resultUnits > 0 {
			multiplier++
		}
	}

	produced := 0
	totalOre := 0
	for produced+current < toCreate {
		for _, parcel := range recipe {
			need := multiplier * parcel.quantity
			parcelChem := parcel.name
			totalOre += s.getCost(need, parcelChem)
		}
		produced += resultUnits * multiplier
	}

	s.amounts[chem] += produced - toCreate
	return totalOre
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

	state := State{make(map[string]int), units, reactions}
	oreNeeded := state.getCost(1, "FUEL")
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

	state := State{make(map[string]int), units, reactions}

	totalFuel := 0
	// try with high fuel amount
	maxTotalFuel := 1000000000000
	minTotalFuel := 0
	oreNeeded := 0
	for {
		totalFuel = (maxTotalFuel + minTotalFuel) / 2
		oreNeeded = state.getCost(totalFuel, "FUEL")
		if oreNeeded > 1000000000000 {
			maxTotalFuel = totalFuel
		} else if oreNeeded < 1000000000000 {
			minTotalFuel = totalFuel
		}
		state = State{make(map[string]int), units, reactions}
		if maxTotalFuel-minTotalFuel <= 1 {
			totalFuel = maxTotalFuel
			break
		}
	}
	oreNeeded = state.getCost(totalFuel, "FUEL")
	if oreNeeded > 1000000000000 {
		totalFuel--
	}
	fmt.Println(totalFuel)
}

// Run day 14
func Run() {
	fmt.Println("-- Day 14 --")
	fmt.Print("Part one output: ")
	part1()
	fmt.Print("Part two output: ")
	part2()
}
