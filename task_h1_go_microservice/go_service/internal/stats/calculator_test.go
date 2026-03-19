package stats_test

import (
	"errors"
	"testing"

	"lab9/task_h1_go_microservice/internal/stats"
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
	if result.Min != 1 {
		t.Errorf("expected min 1, got %v", result.Min)
	}
	if result.Max != 5 {
		t.Errorf("expected max 5, got %v", result.Max)
	}
	if result.Count != 5 {
		t.Errorf("expected count 5, got %v", result.Count)
	}
}

func TestCalculate_Median_OddCount(t *testing.T) {
	result, err := stats.Calculate([]float64{3, 1, 5, 2, 4})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if result.Median != 3 {
		t.Errorf("expected median 3, got %v", result.Median)
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

func TestCalculate_EmptyInput(t *testing.T) {
	_, err := stats.Calculate([]float64{})
	if !errors.Is(err, stats.ErrEmptyInput) {
		t.Errorf("expected ErrEmptyInput, got %v", err)
	}
}

func TestCalculate_SingleElement(t *testing.T) {
	result, err := stats.Calculate([]float64{42})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if result.Min != 42 || result.Max != 42 || result.Mean != 42 {
		t.Errorf("unexpected result for single element: %+v", result)
	}
	if result.Stddev != 0 {
		t.Errorf("expected stddev 0, got %v", result.Stddev)
	}
}
