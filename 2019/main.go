package main

import (
	"os"
	"strconv"

	"github.com/rbusquet/advent-of-code/2019/day1"
	"github.com/rbusquet/advent-of-code/2019/day10"
	"github.com/rbusquet/advent-of-code/2019/day11"
	"github.com/rbusquet/advent-of-code/2019/day12"
	"github.com/rbusquet/advent-of-code/2019/day13"
	"github.com/rbusquet/advent-of-code/2019/day14"
	"github.com/rbusquet/advent-of-code/2019/day15"
	"github.com/rbusquet/advent-of-code/2019/day17"
	"github.com/rbusquet/advent-of-code/2019/day18"
	"github.com/rbusquet/advent-of-code/2019/day19"
	"github.com/rbusquet/advent-of-code/2019/day2"
	"github.com/rbusquet/advent-of-code/2019/day20"
	"github.com/rbusquet/advent-of-code/2019/day21"
	"github.com/rbusquet/advent-of-code/2019/day22"
	"github.com/rbusquet/advent-of-code/2019/day3"
	"github.com/rbusquet/advent-of-code/2019/day4"
	"github.com/rbusquet/advent-of-code/2019/day5"
	"github.com/rbusquet/advent-of-code/2019/day6"
	"github.com/rbusquet/advent-of-code/2019/day7"
	"github.com/rbusquet/advent-of-code/2019/day8"
	"github.com/rbusquet/advent-of-code/2019/day9"
)

func main() {
	handlers := map[string]func(){
		"1":  day1.Run,
		"2":  day2.Run,
		"3":  day3.Run,
		"4":  day4.Run,
		"5":  day5.Run,
		"6":  day6.Run,
		"7":  day7.Run,
		"8":  day8.Run,
		"9":  day9.Run,
		"10": day10.Run,
		"11": day11.Run,
		"12": day12.Run,
		"13": day13.Run,
		"14": day14.Run,
		"15": day15.Run,
		// "16": day16.Run, // tooooo slow
		"17": day17.Run,
		"18": day18.Run,
		"19": day19.Run,
		"20": day20.Run,
		"21": day21.Run,
		"22": day22.Run,
	}
	day := ""
	for idx, arg := range os.Args {
		if arg == "--day" {
			day = os.Args[idx+1]
			break
		}
	}
	if day != "" {
		handlers[day]()
		return
	}
	for i := 1; i <= len(handlers); i++ {
		handlers[strconv.Itoa(i)]()
	}
}
