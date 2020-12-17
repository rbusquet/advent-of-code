package main

type Space map[*[]int]int

func parse3DSpace(initial []string) Space {
	ret := make(map[*[]int]int)
	for x, v := range initial {
		for y, ch := range v {
			position := &[]int{x, y, 0}
			if ch == '.' {
				ret[position] = 0
			} else {
				ret[position] = 1
			}
		}
	}
	return ret
}

func cycle(space Space) Space {
	activeNeighborsCount := make(Space)
}

func main() {
	initial := []string{
		"####.#..",
		".......#",
		"#..#####",
		".....##.",
		"##...###",
		"#..#.#.#",
		".##...#.",
		"#...##..",
	}
	space := parse3DSpace(initial)
}
