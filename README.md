# Лабораторная работа №9 — Вариант 1
## Мультиязычное программирование: Go + Rust + Python

### Задания

| Задание | Язык | Описание |
|---------|------|----------|
| М1 | Go | HTTP-сервер с эндпоинтом `/health` |
| М2 | Go + Python | Go-бинарь с вызовом через subprocess |
| М3 | Rust + Python | Библиотека через PyO3/Maturin |
| В1 | Go + Python | HTTP-микросервис для статистики |
| В2 | Go + Rust + Python | Оркестрация + криптография |

---

### Быстрый старт

#### М1 — Go HTTP-сервер
```bash
cd task_m1_http_server
go test ./...
go run ./cmd/server
# GET http://localhost:8080/health
```

#### М2 — Go subprocess
```bash
cd task_m2_subprocess/go_app
go build -o calculator ./cmd/calculator

cd ../python_client
pip install pytest
pytest test_client.py -v
```

#### М3 — Rust + PyO3
```powershell
# Python 3.14+ требует флага совместимости
$env:PYO3_USE_ABI3_FORWARD_COMPATIBILITY="1"
cargo test
pip install maturin && maturin develop
python python_usage/benchmark.py
```
