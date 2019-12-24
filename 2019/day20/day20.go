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

func buildGrid() (
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
	grid, vertexes := buildGrid()
	sort.Sort(vertexes)
	src, dest, portals := parsePortals(grid, vertexes)
	nodeSrc := utils.NewNode(src, 0)
	queue := []*utils.Node{
		&nodeSrc,
	}
	visited := make(map[utils.Position]bool)
	var node *utils.Node
	for len(queue) > 0 {
		node, queue = queue[0], queue[1:]
		value := node.GetValue().(utils.Position)
		if value == dest {
			fmt.Println(node.GetDistance())
			return
		}
		visited[value] = true

		for neighbor := range value.Surrounds() {
			if visited[neighbor] {
				continue
			}
			if grid[neighbor] == '.' {
				neighborNode := utils.NewNode(neighbor, node.GetDistance()+1)
				queue = append(queue, &neighborNode)
			}
		}
		if otherSide, isPortal := portals[value]; isPortal {
			neighborNode := utils.NewNode(otherSide, node.GetDistance()+1)
			queue = append(queue, &neighborNode)
		}
	}
}

func part2() {
	grid, vertexes := buildGrid()
	sort.Sort(vertexes)
	src, dest, portals := parsePortals(grid, vertexes)
	pq, vertexToNode := initHeap(src, grid, vertexes)
	visited := make(map[utils.Position]bool)

	maxLevel := 0
	for len(pq) > 0 {
		node := heap.Pop(&pq).(*utils.Node)
		value := node.GetValue().(utils.Position)
		visited[value] = true

		for neighbor := range value.Surrounds() {
			if neighbor == dest && value.GetZ() == 0 {
				fmt.Println(node.GetDistance()+1, "hitting max level of recursion", maxLevel)
				return
			}
			if visited[neighbor] {
				continue
			}
			if grid[neighbor.Get2D()] == '.' {
				neighborNode := vertexToNode[neighbor]
				newDistance := node.GetDistance() + 1
				if newDistance < neighborNode.GetDistance() {
					neighborNode.SetDistance(newDistance)
					heap.Fix(&pq, neighborNode.GetIndex())
				}
			}
		}
		if otherSide, isPortal := portals[value.Get2D()]; isPortal {
			if !valid(value) {
				continue
			}
			nextLevel := value.GetZ()
			if isOuter(value.GetX(), value.GetY()) {
				nextLevel--
			} else {
				nextLevel++
			}
			if nextLevel > maxLevel {
				maxLevel = nextLevel
				vertexToNode = pushToHeap(&pq, grid, vertexes, vertexToNode, nextLevel)
			}
			otherSide = otherSide.Get3D(nextLevel)
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

func pushToHeap(
	pq *utils.PriorityQueue,
	grid map[utils.Position]rune,
	vertexes utils.Vector,
	vertexToNode map[utils.Position]*utils.Node,
	level int,
) map[utils.Position]*utils.Node {
	for _, v := range vertexes {
		if grid[v] != '.' {
			continue
		}
		d := math.MaxInt64
		v = v.Get3D(level)
		i := utils.NewNode(v, d)
		heap.Push(pq, &i)
		vertexToNode[v] = &i
	}
	return vertexToNode
}

func valid(pos utils.Position) bool {
	if !isOuter(pos.GetX(), pos.GetY()) {
		return true
	}
	return pos.GetZ() > 0
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
