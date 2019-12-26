package day8

import (
	"fmt"
	"math"

	"github.com/rbusquet/advent-of-code/utils"
)

// Run day 8
func Run() {
	fmt.Println("-- Day 8 --")
	file, scanner := utils.GenerateLineScanner("./day8/input.txt")
	defer (*file).Close()
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
	fmt.Println("Part one output:", output)

	final := []string{}
	for i := 0; i < pixelCount; i++ {
		result := "2"
		for l := 0; l < len(layers); l++ {
			layer := layers[l]
			pixel := layer[i]
			if pixel == "0" || pixel == "1" {
				result = pixel
				break
			}
		}
		final = append(final, result)
	}

	mapper := map[string]string{
		"0": " ",
		"1": "X",
	}
	fmt.Println("Part two output:")
	for index, x := range final {
		if index%width == 0 {
			fmt.Println()
		}
		fmt.Print(mapper[x])
	}
	fmt.Println()
}
