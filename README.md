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
```powershell
cd task_m1_http_server
go test ./...
go run ./cmd/server
# GET http://localhost:8080/health
```

#### М2 — Go subprocess
```powershell
cd task_m2_subprocess\go_app
go build -o calculator.exe ./cmd/calculator

cd ..\python_client
python -m pip install pytest
python -m pytest test_client.py -v
```

#### М3 — Rust + PyO3
```powershell
cd task_m3_rust_lib
$env:PYO3_USE_ABI3_FORWARD_COMPATIBILITY="1"
cargo test
python -m pip install maturin
python -m maturin build --release
python -m pip install target\wheels\fastmath-0.1.0-cp314-cp314-win_amd64.whl --force-reinstall
python python_usage/benchmark.py
```

#### В1 — Go HTTP-микросервис статистики

```powershell
# Терминал 1 — сервис
cd task_h1_go_microservice\go_service
go test ./...
go run ./cmd/service
# слушает на http://localhost:8081/stats

# Терминал 2 — клиент
cd task_h1_go_microservice\python_client
python -m pytest test_client.py -v   # без запущенного сервиса
python client.py                      # живой запрос
```

Формат запроса / ответа:
```json
// POST /stats
{"numbers": [10, 20, 30, 40, 50]}

// Response 200
{"count": 5, "sum": 150, "mean": 30, "median": 30, "min": 10, "max": 50, "stddev": 14.142}
```

#### В2 — Python + Go + Rust (оркестрация + криптография)

```powershell
# Шаг 1 — Rust-библиотека rustcrypto
cd task_h2_orchestration\rust_crypto
$env:PYO3_USE_ABI3_FORWARD_COMPATIBILITY="1"
cargo test
python -m maturin build --release
python -m pip install target\wheels\rustcrypto-0.1.0-cp314-cp314-win_amd64.whl --force-reinstall

# Шаг 2 — Go-сервис (оставить запущенным)
cd ..\go_service
go test ./...
go run ./cmd/service

# Шаг 3 — Python-оркестратор (новый терминал)
cd ..\python_app
python -m pytest test_app.py -v   # без сервиса
python app.py                      # полный цикл
```

Схема взаимодействия:
```
Python Orchestrator
    ├── POST /stats ──► Go-сервис :8082  (статистика)
    └── xor_encrypt() ──► Rust rustcrypto  (XOR-шифрование результата)
```

---

### Структура репозитория

```
lab9_variant1/
├── README.md
├── PROMPT_LOG.md
├── task_m1_http_server/
│   ├── go.mod
│   ├── cmd/server/main.go
│   └── internal/handler/
│       ├── health.go
│       └── health_test.go
├── task_m2_subprocess/
│   ├── go_app/
│   │   ├── go.mod
│   │   └── cmd/calculator/main.go
│   └── python_client/
│       ├── client.py
│       └── test_client.py
├── task_m3_rust_lib/
│   ├── Cargo.toml
│   ├── src/lib.rs
│   └── python_usage/benchmark.py
├── task_h1_go_microservice/
│   ├── go_service/
│   │   ├── go.mod
│   │   ├── cmd/service/main.go
│   │   └── internal/
│   │       ├── stats/calculator.go
│   │       └── handler/stats.go
│   └── python_client/
│       ├── client.py
│       └── test_client.py
└── task_h2_orchestration/
    ├── go_service/
    ├── rust_crypto/
    └── python_app/
```

---

### Требования

| Инструмент | Версия | Примечание |
|-----------|--------|------------|
| Go | 1.21+ | |
| Rust + Cargo | 1.70+ | |
| Python | 3.10+ | При 3.14 нужен флаг PyO3 |
| maturin | любая | `python -m pip install maturin` |
| pytest | любая | `python -m pip install pytest` |

> **Python 3.14+**: перед любой сборкой Rust-библиотек устанавливать:
> ```powershell
> $env:PYO3_USE_ABI3_FORWARD_COMPATIBILITY="1"
> ```
