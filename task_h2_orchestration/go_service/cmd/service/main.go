package main

import (
	"fmt"
	"log"
	"net/http"

	"lab9/task_h2_orchestration/internal/handler"
)

const port = ":8082"

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/stats", handler.StatsHandler)

	fmt.Printf("Orchestration service starting on port %s\n", port)
	log.Fatal(http.ListenAndServe(port, mux))
}
