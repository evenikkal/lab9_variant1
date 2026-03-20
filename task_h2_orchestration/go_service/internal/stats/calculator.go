package stats

import (
	"errors"
	"math"
	"sort"
)

var ErrEmptyInput = errors.New("input must contain at least one number")

type Result struct {
	Count  int     `json:"count"`
	Sum    float64 `json:"sum"`
	Mean   float64 `json:"mean"`
	Median float64 `json:"median"`
	Min    float64 `json:"min"`
	Max    float64 `json:"max"`
	Stddev float64 `json:"stddev"`
}

func Calculate(numbers []float64) (Result, error) {
	if len(numbers) == 0 {
		return Result{}, ErrEmptyInput
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

	return Result{
		Count:  len(numbers),
		Sum:    round(sum),
		Mean:   round(mean),
		Median: median(sorted),
		Min:    sorted[0],
		Max:    sorted[len(sorted)-1],
		Stddev: round(math.Sqrt(variance)),
	}, nil
}

func median(sorted []float64) float64 {
	n := len(sorted)
	if n%2 == 0 {
		return round((sorted[n/2-1] + sorted[n/2]) / 2)
	}
	return sorted[n/2]
}

func round(v float64) float64 {
	return math.Round(v*1000) / 1000
}
