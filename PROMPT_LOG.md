# Prompt Log — Лабораторная работа №9, Вариант 1

> Документирует реальный процесс работы с AI-инструментами при выполнении заданий.
> Инструмент: Claude (claude.ai). Все задания выполнялись итеративно —
> промпты уточнялись по мере возникновения реальных проблем окружения.

---

## Задание М1: Go HTTP-сервер с эндпоинтом /health

### Промпт 1

**Инструмент:** Claude (claude.ai)

**Промпт:**
> "Напиши простой HTTP-сервер на Go с одним эндпоинтом /health, следуя принципам
> чистой архитектуры. Структура: cmd/ для точки входа, internal/handler/ для логики.
> main.go не должен содержать бизнес-логику. Нужны unit-тесты через httptest."

**Результат:** Получила реализацию с чётким разделением:
- `cmd/server/main.go` — только регистрация роутов и запуск
- `internal/handler/health.go` — `HealthHandler` + `HealthResponse` struct
- `health_test.go` — 5 тестов через `httptest.NewRecorder`, без реального порта

Тесты проверяют: статус 200, Content-Type, тело ответа, метод 405.

**Проблема:** VS Code показывал ошибку `initialization failed: no module path` — оказалось,
репозиторий открыт в корне `lab9_variant1`, а Go-модуль находится во вложенной папке.
Решение: открыть `task_m1_http_server` как отдельный workspace.

### Итого

- Количество промптов: 1
- Что пришлось исправлять вручную: открытие правильной папки в VS Code
- Время: ~15 мин
- Результат тестов: `ok lab9/task_m1_http_server/internal/handler 0.241s`

---

## Задание М2: Go-бинарь + Python subprocess

### Промпт 1

**Инструмент:** Claude (claude.ai)

**Промпт:**
> "Напиши Go-программу-калькулятор: читает JSON из stdin (список чисел float64),
> возвращает JSON в stdout с полями sum, mean, min, max, stddev. Логику вычислений
> вынести в отдельную функцию calculate() отдельно от main(). Также напиши Python-клиент
> с классом CalculatorClient и dataclass StatResult. Тесты должны мокировать subprocess.run
> и работать без скомпилированного бинаря."

**Результат:**
- Go: функция `calculate()` полностью независима от `main()`, тестируема в изоляции
- Python: `CalculatorClient` принимает путь к бинарю как зависимость — удобно для тестов
- Тесты мокируют `subprocess.run` через `unittest.mock.patch`

**Проблема 1:** Python не был установлен — установила с python.org, обязательно
с галочкой "Add Python to PATH".

**Проблема 2:** `pytest` не распознавался как команда — запускала через `python -m pytest`.

**Проблема 3:** В файлах `client.py` и `test_client.py` оказался неправильный контент
из-за ошибки при копировании файлов между задачами. Исправила вручную — заменила
содержимое через VS Code.

**Проверка бинаря вручную:**
```powershell
echo '{"numbers":[1,2,3,4,5]}' | .\calculator.exe
# {"sum":15,"mean":3,"min":1,"max":5,"stddev":1.414}
```

### Итого

- Количество промптов: 1
- Что пришлось исправлять вручную: установка Python, содержимое файлов (ошибка копирования)
- Время: ~30 мин
- Результат тестов: `5 passed in 0.12s`

---

## Задание М3: Rust-библиотека через PyO3/Maturin

### Промпт 1

**Инструмент:** Claude (claude.ai)

**Промпт:**
> "Создай Rust-библиотеку fastmath с функцией sum_squares через PyO3.
> Cargo.toml с crate-type cdylib и rlib (rlib нужен для cargo test).
> Логику вынести в sum_squares_impl() без PyO3 — чтобы unit-тесты не зависели
> от Python-окружения. Python-скрипт для бенчмарка Rust vs чистый Python на 10000 элементах."

**Результат:**
- `lib.rs`: публичный `sum_squares()` через `#[pyfunction]` делегирует в приватный `sum_squares_impl()`
- 4 unit-теста в `#[cfg(test)]` — тестируют `impl` напрямую, без PyO3
- `benchmark.py` замеряет скорость на `list(range(1, 10_001))`

**Проблема 1:** PyO3 0.21 не поддерживает Python 3.14 (максимум 3.12).
Обновила версию в `Cargo.toml` до `0.23`.

**Проблема 2:** PyO3 0.23 поддерживает максимум Python 3.13.
Решение: переменная окружения `$env:PYO3_USE_ABI3_FORWARD_COMPATIBILITY="1"` —
использует стабильный ABI без проверки версии.

**Проблема 3:** `cargo test` выдавал `running 0 tests` — тесты не запускались,
потому что `crate-type = ["cdylib"]` не генерирует тестовый бинарь.
Решение: добавить `"rlib"` в список типов.

> **Важно для воспроизведения:** перед `cargo test` и `maturin develop` всегда устанавливать:
> ```powershell
> $env:PYO3_USE_ABI3_FORWARD_COMPATIBILITY="1"
> ```

### Итого

- Количество промптов: 2 (второй — уточнение про rlib и разделение impl/api)
- Что пришлось исправлять вручную: версия PyO3, crate-type, переменная окружения
- Время: ~25 мин
- Результат тестов: `4 passed` (cargo test)

---

## Задание В1: Go HTTP-микросервис для статистики

### Промпт 1

**Инструмент:** Claude (claude.ai)

**Промпт:**
> "Напиши Go HTTP-микросервис на порту 8081 с эндпоинтом POST /stats.
> Принимает JSON {"numbers": [...]} — возвращает count, sum, mean, median, min, max, stddev.
> Три слоя: internal/stats/ — чистая математика без HTTP, internal/handler/ — HTTP-логика,
> cmd/service/ — только запуск. Ошибка на пустом списке — 400 Bad Request.
> Python-клиент StatsServiceClient с dataclass StatsResult. Тесты мокируют urllib."

**Результат:**
- `stats/calculator.go`: функция `Calculate()` возвращает `(Result, error)`, экспортирует `ErrEmptyInput`
- `handler/stats.go`: различает `ErrEmptyInput` (400) и прочие ошибки (500)
- Python: `StatsServiceClient` использует только stdlib — `urllib.request`, без зависимостей
- Тесты Python мокируют `urllib.request.urlopen` через `unittest.mock.patch`

**Проблема:** Файлы Go оказались пустыми после копирования (EOF ошибки).
Заполнила вручную через VS Code.

**Проверка живого сервиса:**
```
# Терминал 1: go run ./cmd/service
# Терминал 2: python client.py
Count:  7 | Mean: 27.143 | Median: 25 | Stddev: 13.054
```

### Итого

- Количество промптов: 1
- Что пришлось исправлять вручную: содержимое Go-файлов (ошибка копирования)
- Время: ~20 мин
- Результат тестов: Go `ok internal/stats`, `ok internal/handler`; Python `5 passed`

---

## Задание В2: Python-оркестратор + Go-микросервис + Rust-криптография

### Промпт 1

**Инструмент:** Claude (claude.ai)

**Промпт:**
> "Реализуй интеграцию трёх компонентов: Python-оркестратор отправляет числа в Go-сервис
> (POST /stats, порт 8082), получает статистику, сериализует результат в JSON,
> шифрует через Rust-библиотеку rustcrypto (XOR + hex-кодирование), возвращает
> зашифрованный и расшифрованный результат. Rust: функции xor_encrypt(text, key) → hex,
> xor_decrypt(hex, key) → text. Python-тесты мокируют HTTP-слой, но реально вызывают Rust."

**Архитектурное решение:**
```
Python Orchestrator
    ├── _fetch_stats()  →  Go :8082/stats  (HTTP)
    └── rustcrypto.xor_encrypt/decrypt()  (FFI через PyO3)
```

**Результат:**
- `rust_crypto/src/lib.rs`: XOR-шифр с hex-кодированием, симметричный — encrypt и decrypt
  используют одну операцию. 4 unit-теста в Rust (roundtrip, hex-формат, разные ключи, пустая строка)
- `python_app/app.py`: класс `Orchestrator` с методом `process()`, возвращает `OrchestratedResult`
- Тесты Python проверяют: roundtrip шифрования, отличие encrypted от plaintext, HTTP-ошибки

**Проблема 1:** `maturin develop` требует virtualenv.
Создала `.venv` в папке `rust_crypto`, но активация через PowerShell заблокирована политикой.
Решение: собрала wheel через `maturin build --release` и установила в системный Python:
```powershell
python -m pip install target\wheels\rustcrypto-0.1.0-cp314-cp314-win_amd64.whl --force-reinstall
```

**Проблема 2:** `rustcrypto` не найден при запуске тестов из `python_app/` —
модуль был установлен только в `.venv`, а не в системный Python.
Решение: то же — установка wheel напрямую.

**Проверка roundtrip:**
```
Encrypted (hex): 1a2f3e4d...
Decrypted:       {"count": 7, "sum": 190.0, "mean": 27.143, ...}
Roundtrip OK:    True
```

### Итого

- Количество промптов: 1
- Что пришлось исправлять вручную: установка Rust-модуля в системный Python вместо venv
- Время: ~35 мин
- Результат тестов: Rust `4 passed`, Go `ok ×2`, Python `5 passed`

---

## Общие наблюдения

**Что работало хорошо:**
- Разделение бизнес-логики и транспортного слоя во всех трёх языках упростило тестирование
- Мокирование на уровне stdlib (`subprocess.run`, `urllib.request.urlopen`) позволило
  писать тесты без поднятия реальных сервисов
- Единый паттерн `dataclass` для DTO в Python обеспечил типобезопасность

**Что потребовало ручного вмешательства:**
- Совместимость PyO3 с Python 3.14 (флаг `PYO3_USE_ABI3_FORWARD_COMPATIBILITY`)
- Установка Rust-модуля в системный Python минуя virtualenv
- Ошибки копирования файлов между задачами (пустые файлы)

**Вывод:** AI-инструменты эффективны для генерации архитектурно-корректного кода,
но реальное окружение (версии интерпретаторов, политики ОС, пути) требует
ручной отладки и понимания происходящего.
