package main

import (
	"fmt"
	"os"
	"testing"

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

func TestAll(t *testing.T) {
	os.Chdir("../")
	handlers := []func(){
		day1.Run,
		day2.Run,
		day3.Run,
		day4.Run,
		day5.Run,
		day6.Run,
		day7.Run,
		day8.Run,
		day9.Run,
		day10.Run,
		day11.Run,
		day12.Run,
		day13.Run,
		day14.Run,
		day15.Run,
		// day16.Run, // tooooo slow
		day17.Run,
		day18.Run,
		day19.Run,
		day20.Run,
		day21.Run,
		day22.Run,
	}
	for _, run := range handlers {
		fmt.Println("ran")
		run()
	}

}
