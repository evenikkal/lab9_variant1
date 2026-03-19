package main

import (
	"fmt"
	"log"
	"net/http"

	"lab9/task_h1_go_microservice/internal/handler"
)

const port = ":8081"

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/stats", handler.StatsHandler)

	fmt.Printf("Stats microservice starting on port %s\n", port)
	log.Fatal(http.ListenAndServe(port, mux))
}
