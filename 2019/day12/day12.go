package main

import (
	"fmt"
	"math"
)

type Vector struct {
	x int
	y int
	z int
}

type Velocity Vector

type Moon struct {
	position *Vector
	velocity *Velocity
}

func (m Moon) String() string {
	return fmt.Sprint(*m.position, *m.velocity)
}

func (m *Moon) applyGravity(other *Moon) {
	m.applyGravityX(other)
	m.applyGravityY(other)
	m.applyGravityZ(other)
}

func (m *Moon) applyGravityX(other *Moon) {
	if m.position.x < other.position.x {
		m.velocity.x++
	} else if m.position.x > other.position.x {
		m.velocity.x--
	}
}

func (m *Moon) applyGravityY(other *Moon) {
	if m.position.y < other.position.y {
		m.velocity.y++
	} else if m.position.y > other.position.y {
		m.velocity.y--
	}
}

func (m *Moon) applyGravityZ(other *Moon) {
	if m.position.z < other.position.z {
		m.velocity.z++
	} else if m.position.z > other.position.z {
		m.velocity.z--
	}
}

func (m *Moon) applyVelocity() {
	m.applyVelocityX()
	m.applyVelocityY()
	m.applyVelocityZ()
}

func (m *Moon) applyVelocityX() { m.position.x += m.velocity.x }
func (m *Moon) applyVelocityY() { m.position.y += m.velocity.y }
func (m *Moon) applyVelocityZ() { m.position.z += m.velocity.z }

func (m *Moon) applySystemGravity(system *[4]*Moon) {
	for _, other := range system {
		m.applyGravity(other)
	}
}

func (m *Moon) applySystemGravityX(system *[4]*Moon) {
	for _, other := range system {
		m.applyGravityX(other)
	}
}
func (m *Moon) applySystemGravityY(system *[4]*Moon) {
	for _, other := range system {
		m.applyGravityY(other)
	}
}
func (m *Moon) applySystemGravityZ(system *[4]*Moon) {
	for _, other := range system {
		m.applyGravityZ(other)
	}
}

func abs(n int) int {
	return int(math.Abs(float64(n)))
}

func (m *Moon) energy() int {
	potential := abs(m.position.x) + abs(m.position.y) + abs(m.position.z)
	kinetic := abs(m.velocity.x) + abs(m.velocity.y) + abs(m.velocity.z)
	return kinetic * potential
}

func part1() {
	// <x=3, y=2, z=-6>
	// <x=-13, y=18, z=10>
	// <x=-8, y=-1, z=13>
	// <x=5, y=10, z=4>
	system := [...]*Moon{
		&(Moon{&Vector{x: 3, y: 2, z: -6}, &Velocity{0, 0, 0}}),
		&(Moon{&Vector{x: -13, y: 18, z: 10}, &Velocity{0, 0, 0}}),
		&(Moon{&Vector{x: -8, y: -1, z: 13}, &Velocity{0, 0, 0}}),
		&(Moon{&Vector{x: 5, y: 10, z: 4}, &Velocity{0, 0, 0}}),
	}

	for index := 0; index < 1000; index++ {
		for _, moon := range system {
			moon.applySystemGravity(&system)
		}
		for _, moon := range system {
			moon.applyVelocity()
		}
	}
	totalEnergy := 0
	for _, moon := range system {
		totalEnergy += moon.energy()
	}
	fmt.Println(totalEnergy)
}

func part2() {
	system := [...]*Moon{
		&(Moon{&Vector{x: 3, y: 2, z: -6}, &Velocity{0, 0, 0}}),
		&(Moon{&Vector{x: -13, y: 18, z: 10}, &Velocity{0, 0, 0}}),
		&(Moon{&Vector{x: -8, y: -1, z: 13}, &Velocity{0, 0, 0}}),
		&(Moon{&Vector{x: 5, y: 10, z: 4}, &Velocity{0, 0, 0}}),
	}

	channel := make(chan int)
	go func(system *[4]*Moon) {
		initial := []int{}
		for _, moon := range system {
			initial = append(initial, moon.position.x)
		}
		fmt.Println("For X: initial is", initial)

		for i := 1; ; i++ {
			for _, moon := range system {
				moon.applySystemGravityX(system)
			}
			for _, moon := range system {
				moon.applyVelocityX()
			}

			same := true
			for idx, moon := range system {
				if moon.position.x != initial[idx] {
					same = false
					break
				}
			}
			if same {
				fmt.Println("Found cycle for X")
				channel <- i
				return
			}
		}
	}(&system)
	go func(system *[4]*Moon) {
		initial := []int{}

		for _, moon := range system {
			initial = append(initial, moon.position.y)
		}
		fmt.Println("For Y: initial is", initial)

		for i := 1; ; i++ {
			for _, moon := range system {
				moon.applySystemGravityY(system)
			}
			for _, moon := range system {
				moon.applyVelocityY()
			}
			same := true
			for idx, moon := range system {
				if moon.position.y != initial[idx] {
					same = false
					break
				}
			}
			if same {
				fmt.Println("Found cycle for Y")
				channel <- i
				return
			}
		}
	}(&system)
	go func(system *[4]*Moon) {
		initial := []int{}
		for _, moon := range system {
			initial = append(initial, moon.position.z)
		}
		fmt.Println("For Z: initial is", initial)

		for i := 1; ; i++ {
			for _, moon := range system {
				moon.applySystemGravityZ(system)
			}
			for _, moon := range system {
				moon.applyVelocityZ()
			}

			same := true
			for idx, moon := range system {
				if moon.position.z != initial[idx] {
					same = false
					break
				}
			}
			if same {
				fmt.Println("Found cycle for Z")
				channel <- i
				return
			}
		}
	}(&system)

	fmt.Println(<-channel)
	fmt.Println(<-channel)
	fmt.Println(<-channel)

}

func main() {
	part1()
	part2()
}
