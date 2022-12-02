package day10

import (
	"fmt"
	"math"
	"sort"

	"github.com/rbusquet/advent-of-code/utils"
)

// Asteroid asts
type Asteroid struct {
	x int
	y int
}

func (a *Asteroid) position() (float64, float64) {
	x, y := float64(a.x), float64(a.y)
	return x, y
}

func (a *Asteroid) distance(other Asteroid) float64 {
	x1, y1 := a.position()
	x2, y2 := other.position()
	x := x2 - x1
	y := y2 - y1
	return math.Sqrt(math.Pow(x, 2) + math.Pow(y, 2))
}

func (a *Asteroid) angle(other Asteroid) float64 {
	x1, y1 := a.position()
	x2, y2 := other.position()
	x := x2 - x1
	y := y2 - y1
	return math.Atan2(x, y)
}

// Run day 10
func Run() {
	fmt.Println("-- Day 10 --")
	file, scanner := utils.GenerateLineScanner("./2019/day10/input.txt")
	defer (*file).Close()
	asteroids := []Asteroid{}
	i := 0
	for scanner.Scan() {
		row := scanner.Text()
		j := 0
		for _, x := range row {
			if string(x) == "#" {
				asteroids = append(asteroids, Asteroid{j, i})
			}
			j++
		}
		i++
	}

	var best Asteroid
	bestCount := 0
	var bestAngles map[float64]*[]Asteroid
	for _, center := range asteroids {
		visited := make(map[float64]*[]Asteroid)
		for _, neighbor := range asteroids {
			if center == neighbor {
				continue
			}
			angle := center.angle(neighbor)
			if _, ok := visited[angle]; ok {
				*visited[angle] = append(*visited[angle], neighbor)
			} else {
				first := []Asteroid{neighbor}
				visited[angle] = &first
			}
		}
		if len(visited) > bestCount {
			bestCount = len(visited)
			bestAngles = visited
			best = center
		}
	}
	fmt.Println("Part one output:", bestCount)

	angles := []float64{}
	for angle := range bestAngles {
		angles = append(angles, angle)
	}
	sort.Float64s(angles)

	pi := math.Pi
	firstIteration := 0
	for index, angle := range angles {
		if angle < pi {
			firstIteration = index
		} else {
			firstIteration = index
			break
		}
	}

	destroyed := 0
	for {
		index := firstIteration % len(angles)
		asteroids := *bestAngles[angles[index]]

		if len(asteroids) > 0 {
			min := math.MaxFloat64
			var closest Asteroid
			var closestIndex int
			for di, asteroid := range asteroids {
				distance := best.distance(asteroid)
				if distance < min {
					min = distance
					closestIndex = di
					closest = asteroid
				}
			}
			asteroids = append(asteroids[:closestIndex], asteroids[closestIndex+1:]...)
			bestAngles[angles[index]] = &asteroids
			destroyed++
			if destroyed == 200 {
				fmt.Println("Part two output:", closest.x*100+closest.y)
				return
			}
		}
		firstIteration--
	}
}
