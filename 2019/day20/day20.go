package day20

import (
	"advent-of-code/2019/utils"
	"container/heap"
	"fmt"
	"math"
	"sort"
)

func isAlpha(s rune) bool {
	return 'A' <= s && s <= 'Z'
}

func buildGrid(filename string) (
	map[utils.Position]rune,
	utils.Vector,
) {
	file, scanner := utils.GenerateLineScanner("./day20/input.txt")
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

func initHeap(
	src utils.Position,
	grid map[utils.Position]rune,
	vertexes utils.Vector,
) (
	utils.PriorityQueue,
	map[utils.Position]*utils.Node,
) {
	pq := make(utils.PriorityQueue, 0)
	vertexToNode := make(map[utils.Position]*utils.Node)
	heap.Init(&pq)
	for _, v := range vertexes {
		if grid[v] != '.' {
			continue
		}
		d := math.MaxInt64
		if v == src {
			d = 0
		}
		i := utils.NewNode(v, d)
		heap.Push(&pq, &i)
		vertexToNode[v] = &i
	}
	return pq, vertexToNode
}

func part1() {
	grid, vertexes := buildGrid("./input.txt")
	sort.Sort(vertexes)
	src, dest, portals := parsePortals(grid, vertexes)
	pq, vertexToNode := initHeap(src, grid, vertexes)
	visited := make(map[utils.Position]bool)

	for len(pq) > 0 {
		node := heap.Pop(&pq).(*utils.Node)
		value := node.GetValue().(utils.Position)
		visited[value] = true

		for neighbor := range value.Surrounds() {
			if visited[neighbor] {
				continue
			}
			if grid[neighbor] == '.' {
				neighborNode := vertexToNode[neighbor]
				newDistance := node.GetDistance() + 1
				if newDistance < neighborNode.GetDistance() {
					neighborNode.SetDistance(newDistance)
					heap.Fix(&pq, neighborNode.GetIndex())
				}
			}
		}
		if otherSide, isPortal := portals[value]; isPortal {
			neighborNode := vertexToNode[otherSide]
			newDistance := node.GetDistance() + 1
			if newDistance < neighborNode.GetDistance() {
				neighborNode.SetDistance(newDistance)
				heap.Fix(&pq, neighborNode.GetIndex())
			}
		}
	}
	fmt.Println(vertexToNode[dest].GetDistance())
}

// Run day 20
func Run() {
	fmt.Println("-- Day 20 --")
	fmt.Print("Part one output: ")
	part1()
}
