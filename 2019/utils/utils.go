package utils

import (
	"bufio"
	"os"
	"path/filepath"
	"strconv"
	"strings"
)

// GenerateLineScanner generates
func GenerateLineScanner(fileName string) (*os.File, *bufio.Scanner) {
	if path, err := filepath.Abs(fileName); err != nil {
		panic(err)
	} else {
		if file, err := os.Open(path); err != nil {
			panic(err)
		} else {
			scanner := bufio.NewScanner(file)
			return file, scanner
		}
	}
}

func splitOnDigit(data []byte, atEOF bool) (advance int, token []byte, err error) {
	if len(data) == 2 && data[1] == '\n' {
		return 1, data[:1], bufio.ErrFinalToken
	} else if len(data) == 1 {
		return 1, data[:1], bufio.ErrFinalToken
	}
	return 1, data[:1], nil
}

func splitOnComma(data []byte, atEOF bool) (advance int, token []byte, err error) {
	for i := 0; i < len(data); i++ {
		if data[i] == ',' {
			return i + 1, data[:i], nil
		}
	}
	if !atEOF {
		return 0, nil, nil
	}
	// There is one final token to be delivered, which may be the empty string.
	// Returning bufio.ErrFinalToken here tells Scan there are no more tokens after this
	// but does not trigger an error to be returned from Scan itself.
	return 0, data, bufio.ErrFinalToken
}

// GenerateCommaSeparatedScanner comma separated
func GenerateCommaSeparatedScanner(fileName string) (*os.File, *bufio.Scanner) {
	file, scanner := GenerateLineScanner(fileName)

	scanner.Split(splitOnComma)
	return file, scanner
}

// DigitSeparatedScanner each digit at a time
func DigitSeparatedScanner(fileName string) (*os.File, *bufio.Scanner) {
	file, scanner := GenerateLineScanner(fileName)

	scanner.Split(splitOnDigit)
	return file, scanner
}

// Permutations returns permutations
// From https://en.wikipedia.org/wiki/Heap%27s_algorithm#Details_of_the_algorithm
func Permutations(input []int, size int) [][]int {
	if size == 1 {
		return [][]int{append([]int{}, input...)}
	}
	results := Permutations(input, size-1)
	for i := 0; i < size-1; i++ {
		if size%2 == 0 {
			input[i], input[size-1] = input[size-1], input[i]
		} else {
			input[0], input[size-1] = input[size-1], input[0]
		}
		results = append(results, Permutations(input, size-1)...)
	}
	return results
}

// ReadProgram reads an IntCode program from a file
func ReadProgram(filename string) (program []int) {
	memory := []int{}
	file, scanner := GenerateCommaSeparatedScanner(filename)
	for scanner.Scan() {
		if val, err := strconv.Atoi(strings.TrimSpace(scanner.Text())); err == nil {
			memory = append(memory, val)
		}
	}
	file.Close()
	return memory
}

// AbsInt is an abs implementation for integers
func AbsInt(v int64) int64 {
	if v < 0 {
		return -v
	}
	return v
}

// Sum adds the int values in an slice
func Sum(items ...int) int {
	initial := 0
	for i := range items {
		initial += items[i]
	}
	return initial
}

// GCD returns the greated common divisor for two integers
func GCD(a, b int64) int64 {
	if a > b {
		return GCD(a-b, b)
	}
	if b > a {
		return GCD(a, b-a)
	}
	return a
}

// LCM returns lower common multiplier for two integers
func LCM(a, b int64) int64 {
	return AbsInt(a*b) / GCD(a, b)
}

// Position in a 2D plane
type Position struct {
	x, y int
}

// GetX returns the x value of p
func (p Position) GetX() int {
	return p.x
}

// GetY returns the y value of p
func (p Position) GetY() int {
	return p.y
}

// NewPosition returns a new position
func NewPosition(x, y int) Position {
	return Position{x, y}
}

// Surrounds are the points around p, excluding diagonals
func (p Position) Surrounds() chan Position {
	output := make(chan Position)

	go func() {
		output <- Position{p.x - 1, p.y}
		output <- Position{p.x + 1, p.y}
		output <- Position{p.x, p.y - 1}
		output <- Position{p.x, p.y + 1}
		close(output)
	}()
	return output
}
