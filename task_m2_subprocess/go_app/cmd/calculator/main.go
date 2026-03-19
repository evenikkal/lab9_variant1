package main

import (
	"encoding/json"
	"fmt"
	"math"
	"os"
	"sort"
)

type Input struct {
	Numbers []float64 `json:"numbers"`
}

type Output struct {
	Sum    float64 `json:"sum"`
	Mean   float64 `json:"mean"`
	Min    float64 `json:"min"`
	Max    float64 `json:"max"`
	Stddev float64 `json:"stddev"`
}

func calculate(numbers []float64) Output {
	if len(numbers) == 0 {
		return Output{}
	}

	sorted := make([]float64, len(numbers))
	copy(sorted, numbers)
	sort.Float64s(sorted)

	sum := 0.0
	for _, n := range numbers {
		sum += n
	}
	mean := sum / float64(len(numbers))

	variance := 0.0
	for _, n := range numbers {
		diff := n - mean
		variance += diff * diff
	}
	variance /= float64(len(numbers))

	return Output{
		Sum:    math.Round(sum*1000) / 1000,
		Mean:   math.Round(mean*1000) / 1000,
		Min:    sorted[0],
		Max:    sorted[len(sorted)-1],
		Stddev: math.Round(math.Sqrt(variance)*1000) / 1000,
	}
}

func main() {
	var input Input
	if err := json.NewDecoder(os.Stdin).Decode(&input); err != nil {
		fmt.Fprintf(os.Stderr, "error decoding input: %v\n", err)
		os.Exit(1)
	}

	result := calculate(input.Numbers)

	if err := json.NewEncoder(os.Stdout).Encode(result); err != nil {
		fmt.Fprintf(os.Stderr, "error encoding output: %v\n", err)
		os.Exit(1)
	}
}
