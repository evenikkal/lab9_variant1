// Package handler содержит HTTP-обработчики сервера.
package handler

import (
	"encoding/json"
	"net/http"
	"time"
)

// HealthResponse — структура ответа эндпоинта /health.
type HealthResponse struct {
	Status    string `json:"status"`
	Timestamp string `json:"timestamp"`
	Service   string `json:"service"`
}

// NewHealthResponse создаёт новый HealthResponse с текущим временем.
func NewHealthResponse() HealthResponse {
	return HealthResponse{
		Status:    "ok",
		Timestamp: time.Now().UTC().Format(time.RFC3339),
		Service:   "lab9-http-server",
	}
}

// HealthHandler обрабатывает GET /health и возвращает статус сервиса.
func HealthHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}

	response := NewHealthResponse()

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(response) //nolint:errcheck
}
