package handler

import (
	"encoding/json"
	"errors"
	"net/http"

	"lab9/task_h1_go_microservice/internal/stats"
)

type StatsRequest struct {
	Numbers []float64 `json:"numbers"`
}

type ErrorResponse struct {
	Error string `json:"error"`
}

func StatsHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		writeError(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req StatsRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeError(w, "invalid JSON body", http.StatusBadRequest)
		return
	}

	result, err := stats.Calculate(req.Numbers)
	if err != nil {
		if errors.Is(err, stats.ErrEmptyInput) {
			writeError(w, err.Error(), http.StatusBadRequest)
			return
		}
		writeError(w, "internal error", http.StatusInternalServerError)
		return
	}

	writeJSON(w, result, http.StatusOK)
}

func writeJSON(w http.ResponseWriter, v any, status int) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(v)
}

func writeError(w http.ResponseWriter, msg string, status int) {
	writeJSON(w, ErrorResponse{Error: msg}, status)
}
