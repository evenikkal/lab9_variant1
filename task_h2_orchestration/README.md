# Задание В2 — Python + Go + Rust

## Архитектура

```
Python (оркестратор)
    │
    ├── POST /stats ──► Go-сервис (порт 8082)
    │                   статистика: sum, mean, median, stddev...
    │
    └── xor_encrypt() ──► Rust-библиотека (rustcrypto)
                          XOR-шифрование результата
```

## Быстрый старт

### 1. Собрать Rust-библиотеку
```powershell
cd rust_crypto
$env:PYO3_USE_ABI3_FORWARD_COMPATIBILITY="1"
cargo test
pip install maturin
maturin develop
```

### 2. Запустить Go-сервис
```powershell
cd go_service
go test ./...
go run ./cmd/service
```

### 3. Запустить Python-оркестратор (в новом терминале)
```powershell
cd python_app
python app.py
```

### 4. Запустить Python-тесты
```powershell
cd python_app
python -m pytest test_app.py -v
```