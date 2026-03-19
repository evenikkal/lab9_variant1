package handler_test

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"lab9/task_h1_go_microservice/internal/handler"
	"lab9/task_h1_go_microservice/internal/stats"
)

func TestStatsHandler_ValidInput(t *testing.T) {
	body := `{"numbers":[1,2,3,4,5]}`
	req := httptest.NewRequest(http.MethodPost, "/stats", bytes.NewBufferString(body))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()

	handler.StatsHandler(rec, req)

	if rec.Code != http.StatusOK {
		t.Errorf("expected 200, got %d", rec.Code)
	}

	var result stats.Result
	if err := json.NewDecoder(rec.Body).Decode(&result); err != nil {
		t.Fatalf("failed to decode response: %v", err)
	}
	if result.Sum != 15 {
		t.Errorf("expected sum 15, got %v", result.Sum)
	}
	if result.Mean != 3 {
		t.Errorf("expected mean 3, got %v", result.Mean)
	}
}

func TestStatsHandler_EmptyNumbers(t *testing.T) {
	body := `{"numbers":[]}`
	req := httptest.NewRequest(http.MethodPost, "/stats", bytes.NewBufferString(body))
	rec := httptest.NewRecorder()

	handler.StatsHandler(rec, req)

	if rec.Code != http.StatusBadRequest {
		t.Errorf("expected 400, got %d", rec.Code)
	}
}

func TestStatsHandler_InvalidJSON(t *testing.T) {
	req := httptest.NewRequest(http.MethodPost, "/stats", bytes.NewBufferString("not json"))
	rec := httptest.NewRecorder()

	handler.StatsHandler(rec, req)

	if rec.Code != http.StatusBadRequest {
		t.Errorf("expected 400, got %d", rec.Code)
	}
}

func TestStatsHandler_MethodNotAllowed(t *testing.T) {
	req := httptest.NewRequest(http.MethodGet, "/stats", nil)
	rec := httptest.NewRecorder()

	handler.StatsHandler(rec, req)

	if rec.Code != http.StatusMethodNotAllowed {
		t.Errorf("expected 405, got %d", rec.Code)
	}
}
