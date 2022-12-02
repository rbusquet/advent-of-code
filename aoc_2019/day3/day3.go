package day3

import (
	"fmt"
	"math"
	"strconv"
	"strings"

	"github.com/rbusquet/advent-of-code/utils"
)

// Point (x, y)
type Point struct {
	x int
	y int
}

func wireLocations(wire string) map[Point]int {
	points := make(map[Point]int)
	lastPoint := Point{0, 0}
	steps := 0
	for _, command := range strings.Split(wire, ",") {
		direction := command[:1]
		amount, _ := strconv.Atoi(command[1:])

		lastX := lastPoint.x
		lastY := lastPoint.y
		switch direction {
		case "R":
			{
				for index := 1; index <= amount; index++ {
					steps++
					newPoint := Point{lastX + index, lastY}
					if points[newPoint] == 0 {
						points[newPoint] = steps
					}
					lastPoint = newPoint
				}
			}
		case "L":
			{
				for index := 1; index <= amount; index++ {
					steps++
					newPoint := Point{lastX - index, lastY}
					if points[newPoint] == 0 {
						points[newPoint] = steps
					}
					lastPoint = newPoint
				}
			}
		case "U":
			{
				for index := 1; index <= amount; index++ {
					steps++
					newPoint := Point{lastX, lastY + index}
					if points[newPoint] == 0 {
						points[newPoint] = steps
					}
					lastPoint = newPoint
				}
			}
		case "D":
			{
				for index := 1; index <= amount; index++ {
					steps++
					newPoint := Point{lastX, lastY - index}
					if points[newPoint] == 0 {
						points[newPoint] = steps
					}
					lastPoint = newPoint
				}
			}
		}
	}

	return points
}

// Run day 3
func Run() {
	fmt.Println("-- Day 3 --")
	file, scanner := utils.GenerateLineScanner("./2019/day3/input.txt")
	defer (*file).Close()
	scanner.Scan()
	wireA := scanner.Text()
	scanner.Scan()
	wireB := scanner.Text()
	pointsA := wireLocations(wireA)
	pointsB := wireLocations(wireB)

	minDistance := math.MaxFloat64

	for point := range pointsB {
		if pointsA[point] > 0 {
			// fmt.Println("Found!")
			if min := math.Abs(float64(point.x)) + math.Abs(float64(point.y)); min < minDistance {
				minDistance = min
			}
		}
	}
	fmt.Println("Part one output:", minDistance)

	minDistanceI := math.MaxInt64
	for point, steps := range pointsB {
		if pointsA[point] > 0 {
			// fmt.Println("Found!")
			if min := pointsA[point] + steps; min < minDistanceI {
				minDistanceI = min
			}
		}
	}
	fmt.Println("Part two output:", minDistanceI)
}
