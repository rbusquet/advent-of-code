package day12

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/rbusquet/advent-of-code/utils"
)

// Moon holds position and velocity information of a moon
type Moon struct {
	position []int64
	velocity []int64
}

// NewMoon returns a moon from a line in the format `<x=X, y=Y, z=Z>`
func NewMoon(line string) *Moon {
	moon := Moon{[]int64{}, []int64{0, 0, 0}}
	line = strings.Trim(line, ">")
	for _, bit := range strings.Split(line, ",") {
		val, _ := strconv.Atoi(strings.Split(bit, "=")[1])
		moon.position = append(moon.position, int64(val))
	}
	return &moon
}

func (m *Moon) applyAxisGravity(system []*Moon, axis int) {
	for _, moon := range system {
		if m.position[axis] < moon.position[axis] {
			m.velocity[axis]++
		} else if m.position[axis] > moon.position[axis] {
			m.velocity[axis]--
		}
	}
}

func (m *Moon) applyGravity(system []*Moon) {
	for axis := 0; axis < 3; axis++ {
		m.applyAxisGravity(system, axis)
	}
}

func (m *Moon) applyAxisSpeed(axis int) {
	m.position[axis] += m.velocity[axis]
}

func (m *Moon) applySpeed() {
	for axis := 0; axis < 3; axis++ {
		m.applyAxisSpeed(axis)
	}
}

func (m *Moon) totalEnergy() int64 {
	potential := int64(0)
	for axis := 0; axis < 3; axis++ {
		potential += utils.AbsInt(m.position[axis])
	}
	kinectic := int64(0)
	for axis := 0; axis < 3; axis++ {
		kinectic += utils.AbsInt(m.velocity[axis])
	}
	return potential * kinectic
}

func part1() {
	system := []*Moon{}
	file, scanner := utils.GenerateLineScanner("./day12/input.txt")
	defer (*file).Close()
	for scanner.Scan() {
		moon := NewMoon(scanner.Text())
		system = append(system, moon)
	}

	for i := 0; i < 1000; i++ {
		for _, moon := range system {
			moon.applyGravity(system)
		}
		for _, moon := range system {
			moon.applySpeed()
		}
	}
	energy := int64(0)
	for _, moon := range system {
		energy += moon.totalEnergy()
	}

	fmt.Println("Part one output:", energy)
}

func part2() {
	system := []*Moon{}
	file, scanner := utils.GenerateLineScanner("./day12/input.txt")
	defer (*file).Close()
	for scanner.Scan() {
		moon := NewMoon(scanner.Text())
		system = append(system, moon)
	}

	channel := make(chan int64)
	for axis := 0; axis < 3; axis++ {
		go func(axis int) {
			currentpos := []int64{}
			currentvel := []int64{}
			for _, moon := range system {
				currentpos = append(currentpos, moon.position[axis])
				currentvel = append(currentvel, moon.velocity[axis])
			}
		loop:
			for i := int64(1); ; i++ {
				for _, moon := range system {
					moon.applyAxisGravity(system, axis)
				}
				for _, moon := range system {
					moon.applyAxisSpeed(axis)
				}
				for idx, moon := range system {
					if currentpos[idx] != moon.position[axis] {
						continue loop
					}
					if currentvel[idx] != moon.velocity[axis] {
						continue loop
					}
				}
				channel <- i
				break loop
			}
		}(axis)
	}

	lcm := utils.LCM(utils.LCM(<-channel, <-channel), <-channel)
	fmt.Println("Part two output:", lcm)
}

// Run day 12
func Run() {
	fmt.Println("-- Day 12 --")
	part1()
	part2()
}
