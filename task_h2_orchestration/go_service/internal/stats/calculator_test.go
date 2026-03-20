package stats_test

import (
	"errors"
	"testing"

	"lab9/task_h2_orchestration/internal/stats"
)

func TestCalculate_BasicCase(t *testing.T) {
	result, err := stats.Calculate([]float64{1, 2, 3, 4, 5})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if result.Sum != 15 {
		t.Errorf("expected sum 15, got %v", result.Sum)
	}
	if result.Mean != 3 {
		t.Errorf("expected mean 3, got %v", result.Mean)
	}
}

func TestCalculate_EmptyInput(t *testing.T) {
	_, err := stats.Calculate([]float64{})
	if !errors.Is(err, stats.ErrEmptyInput) {
		t.Errorf("expected ErrEmptyInput, got %v", err)
	}
}

func TestCalculate_Median_EvenCount(t *testing.T) {
	result, err := stats.Calculate([]float64{1, 2, 3, 4})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if result.Median != 2.5 {
		t.Errorf("expected median 2.5, got %v", result.Median)
	}
}
