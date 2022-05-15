package utils

import (
	"bufio"
	"os"
	"path/filepath"
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
func Permutations[T any](input []T, size int) [][]T {
	if size == 1 {
		return [][]T{append([]T{}, input...)}
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

// AbsInt is an abs implementation for integers
func AbsInt(v int) int {
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
func GCD(a, b int) int {
	if a > b {
		return GCD(a-b, b)
	}
	if b > a {
		return GCD(a, b-a)
	}
	return a
}

// LCM returns lower common multiplier for two integers
func LCM(a, b int) int {
	return AbsInt(a*b) / GCD(a, b)
}

// Position in a 2D plane
type Position struct {
	x, y, z int
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
	return Position{x, y, 0}
}

// New3DPosition returns a new position
func New3DPosition(x, y, z int) Position {
	return Position{x, y, z}
}

// Surrounds are the points around p, excluding diagonals
func (p Position) Surrounds() chan Position {
	output := make(chan Position)

	go func() {
		output <- Position{p.x - 1, p.y, p.z}
		output <- Position{p.x + 1, p.y, p.z}
		output <- Position{p.x, p.y - 1, p.z}
		output <- Position{p.x, p.y + 1, p.z}
		close(output)
	}()
	return output
}

// Vector is an array of positions
type Vector []Position

func (a Vector) Len() int      { return len(a) }
func (a Vector) Swap(i, j int) { a[i], a[j] = a[j], a[i] }
func (a Vector) Less(i, j int) bool {
	if a[i].x == a[j].x {
		return a[i].y < a[j].y
	}
	return a[i].x < a[j].x
}

// Get2D returns the position with Z == 0
func (p Position) Get2D() Position {
	return Position{p.GetX(), p.GetY(), 0}
}

// Get3D returns the position with Z == z
func (p Position) Get3D(z int) Position {
	return Position{p.GetX(), p.GetY(), z}
}

// GetZ returns the z portion of this position
func (p Position) GetZ() int {
	return p.z
}
