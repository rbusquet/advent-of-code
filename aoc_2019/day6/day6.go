package day6

import (
	"fmt"
	"strings"

	"github.com/rbusquet/advent-of-code/utils"
)

// Planet represents each node in the orbits map
type Planet struct {
	name   string
	parent string
}

// Universe holds state for the whole orbits map
type Universe struct {
	objects map[string]*Planet
}

func (u *Universe) getObject(name string) *Planet {
	if _, exists := u.objects[name]; !exists {
		planet := Planet{name: name}
		u.objects[name] = &planet
		// return &planet
	}
	planet := u.objects[name]
	return planet
}

func (u *Universe) countPlanetOrbits(planet string) int {
	p := u.getObject(planet)
	if p.parent == "" {
		return 0
	}
	return 1 + u.countPlanetOrbits(p.parent)
}

func (u *Universe) countOrbits() int {
	count := 0
	for _, planet := range u.objects {
		count += u.countPlanetOrbits(planet.name)
	}
	return count
}

func (u *Universe) getDistance(from string, to string) int {
	you := u.getObject(from)
	youParent := u.getObject(you.parent)

	youPath := []string{youParent.name}
	visited := make(map[string]bool)
	for youParent.parent != "" {
		visited[youParent.parent] = true
		youPath = append(youPath, youParent.parent)
		youParent = u.getObject(youParent.parent)
	}
	youToCommon := 0
	santaToCommon := 0
	santa := u.getObject(to)
	santaParent := u.getObject(santa.parent)
	for santaParent.parent != "" {
		if visited[santaParent.parent] {
			youToCommon = 0
			for index := 0; youPath[index] != santaParent.parent; index++ {
				youToCommon++
			}
			break
		}
		santaToCommon++
		santaParent = u.getObject(santaParent.parent)
	}
	return youToCommon + santaToCommon + 1 // account for common planet step
}

// Run day 6
func Run() {
	fmt.Println("-- Day 5 --")
	file, scanner := utils.GenerateLineScanner("./2019/day6/input.txt")
	defer (*file).Close()
	planets := make(map[string]*Planet)
	universe := Universe{planets}
	for scanner.Scan() {
		line := strings.Split(scanner.Text(), ")")
		parent := universe.getObject(line[0])
		child := universe.getObject(line[1])
		child.parent = parent.name
	}
	fmt.Println("Part one output:", universe.countOrbits())
	count := universe.getDistance("YOU", "SAN")
	fmt.Println("Part one output:", count)
}
