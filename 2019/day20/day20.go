package day20

import (
	"fmt"
	"sort"

	"github.com/rbusquet/advent-of-code/utils"
)

// Node is a node in the queue
type Node struct {
	position utils.Position
	distance int
}

func isAlpha(s rune) bool {
	return 'A' <= s && s <= 'Z'
}

func buildGrid() (
	map[utils.Position]rune,
	utils.Vector,
) {
	file, scanner := utils.GenerateLineScanner("./2019/day20/input.txt")
	defer file.Close()
	y := 0

	grid := make(map[utils.Position]rune)
	vertexes := []utils.Position{}
	for scanner.Scan() {
		for x, s := range scanner.Text() {
			pos := utils.NewPosition(x, y)
			grid[pos] = s
			vertexes = append(vertexes, pos)
		}
		y++
	}
	return grid, vertexes
}

func parsePortals(
	grid map[utils.Position]rune,
	vertexes utils.Vector,
) (
	utils.Position,
	utils.Position,
	map[utils.Position]utils.Position,
) {
	counter := 0
	var src, dest utils.Position
	portals := make(map[utils.Position]utils.Position)
	labelToPortal := make(map[string]utils.Position)
	for _, pos := range vertexes {
		counter++
		var portal utils.Position
		label := ""
		if isAlpha(grid[pos]) {
			for p := range pos.Surrounds() {
				if grid[p] == '.' {
					portal = p
				} else if isAlpha(grid[p]) {
					label = string(grid[pos]) + string(grid[p])
					// try finding potential portal on p
					for pp := range p.Surrounds() {
						if grid[pp] == '.' {
							portal = pp
							break
						}
					}
					grid[p] = ' '
				}
			}
			if label == "AA" {
				src = portal
			} else if label == "ZZ" {
				dest = portal
			}
			if otherPortal, exists := labelToPortal[label]; exists {
				portals[portal] = otherPortal
				portals[otherPortal] = portal
			} else {
				labelToPortal[label] = portal
			}
		}
	}
	return src, dest, portals
}

func part1() {
	grid, vertexes := buildGrid()
	sort.Sort(vertexes)
	src, dest, portals := parsePortals(grid, vertexes)
	nodeSrc := Node{src, 0}
	queue := []Node{nodeSrc}

	visited := make(map[utils.Position]bool)
	var node Node
	for len(queue) > 0 {
		node, queue = queue[0], queue[1:]
		value := node.position
		if value == dest {
			fmt.Println(node.distance)
			return
		}
		visited[value] = true

		for neighbor := range value.Surrounds() {
			if visited[neighbor] {
				continue
			}
			if grid[neighbor] == '.' {
				neighborNode := Node{neighbor, node.distance + 1}
				queue = append(queue, neighborNode)
			}
		}
		if otherSide, isPortal := portals[value]; isPortal {
			neighborNode := Node{otherSide, node.distance + 1}
			queue = append(queue, neighborNode)
		}
	}
}

func part2() {
	grid, vertexes := buildGrid()
	sort.Sort(vertexes)
	src, dest, portals := parsePortals(grid, vertexes)
	visited := make(map[utils.Position]bool)
	nodeSrc := Node{src, 0}
	queue := []Node{nodeSrc}

	var node Node
	for len(queue) > 0 {
		node, queue = queue[0], queue[1:]
		value := node.position
		if value == dest {
			fmt.Println(node.distance)
			return
		}
		visited[value] = true

		for neighbor := range value.Surrounds() {
			if visited[neighbor] {
				continue
			}
			if grid[neighbor.Get2D()] == '.' {
				newNode := Node{neighbor, node.distance + 1}
				queue = append(queue, newNode)
			}
		}
		if otherSide, isPortal := portals[value.Get2D()]; isPortal {
			nextLevel := value.GetZ()
			if isOuter(value.GetX(), value.GetY()) {
				nextLevel--
			} else {
				nextLevel++
			}
			if nextLevel < 0 {
				continue
			}
			otherSide = otherSide.Get3D(nextLevel)
			if visited[otherSide] {
				continue
			}
			visited[otherSide] = true
			newNode := Node{otherSide, node.distance + 1}
			queue = append(queue, newNode)
		}
	}
}

func isOuter(x, y int) bool {
	return x < 4 || x > 123 || y < 3 || y > 117
}

// Run day 20
func Run() {
	fmt.Println("-- Day 20 --")
	fmt.Print("Part one output: ")
	part1()
	fmt.Print("Part two output: ")
	part2()
}
