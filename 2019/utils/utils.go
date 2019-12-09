package utils

import (
	"bufio"
	"os"
	"path/filepath"
)

// GenerateLineScanner generates
func GenerateLineScanner(fileName string) *bufio.Scanner {
	if path, err := filepath.Abs(fileName); err != nil {
		panic(err)
	} else {
		if file, err := os.Open(path); err != nil {
			panic(err)
		} else {
			scanner := bufio.NewScanner(file)
			return scanner
		}
	}
}

// GenerateCommaSeparatedScanner comma separated
func GenerateCommaSeparatedScanner(fileName string) *bufio.Scanner {
	scanner := GenerateLineScanner(fileName)
	onComma := func(data []byte, atEOF bool) (advance int, token []byte, err error) {
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
	scanner.Split(onComma)
	return scanner
}

// Permutations returns permutations
// From https://en.wikipedia.org/wiki/Heap%27s_algorithm#Details_of_the_algorithm
func Permutations(input []int, size int) [][]int {
	if size == 1 {
		return [][]int{append([]int{}, input...)}
	}
	results := Permutations(input, size - 1)
	for i := 0; i < size-1; i++ {
		if size % 2 == 0 {
			input[i], input[size-1] = input[size-1], input[i]
		} else {
			input[0], input[size-1] = input[size-1], input[0]
		}
		results = append(results, Permutations(input, size-1)...)
	}
	return results
}
