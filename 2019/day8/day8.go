package main

import (
	"advent-of-code/2019/utils"
	"fmt"
	"math"
)

func main() {
	scanner := utils.GenerateLineScanner("./input.txt")
	scanner.Scan()
	row := scanner.Text()

	layers := make(map[int][]string)

	width, height := 25, 6

	pixelCount := width * height

	count := make(map[string]map[int]int)
	i := 0
	for _, r := range row {
		x := string(r)
		layerID := i / pixelCount
		layer := layers[layerID]
		layers[layerID] = append(layer, x)
		if _, ok := count[x]; !ok {
			count[x] = make(map[int]int)
		}
		count[x][layerID]++
		i++
	}

	max := math.MaxInt64
	chosenLayer := -1
	for layerID, zeroCount := range count["0"] {
		if zeroCount < max {
			chosenLayer = layerID
			max = zeroCount
		}
	}
	output := count["1"][chosenLayer] * count["2"][chosenLayer]
	fmt.Println(output)

	final := []string{}
	for i := 0; i < pixelCount; i++ {
		result := "2"
		for l := len(layers) - 1; l >= 0; l-- {
			layer := layers[l]
			switch layer[i] {
			case "2":
				continue
			case "0":
				{
					result = "0"
					break
				}
			case "1":
				{
					result = "1"
					break
				}
			}
		}
		final = append(final, result)
	}

	mapper := map[string]string{
		"0": " ",
		"1": "X",
	}
	for index, x := range final {
		if index%25 == 0 {
			fmt.Println()
		}
		fmt.Print(mapper[x])
	}
	// Output: HCGFE
	// X  X  XX   XX  XXXX XXXX
	// X  X X  X X  X X    X
	// XXXX X    X    XXX  XXX
	// X  X X    X XX X    X
	// X  X X  X X  X X    X
	// X  X  XX   XXX X    XXXX
}
