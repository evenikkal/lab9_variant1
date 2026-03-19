package main

import (
	"fmt"
	"log"
	"net/http"

	"lab9/task_m1_http_server/internal/handler"
)

const port = ":8080"

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/health", handler.HealthHandler)

	fmt.Printf("Server starting on port %s\n", port)
	log.Fatal(http.ListenAndServe(port, mux))
}
