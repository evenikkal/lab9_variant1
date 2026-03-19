from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path


BINARY_PATH = Path(__file__).parent.parent / "go_app" / "calculator.exe"


@dataclass(frozen=True)
class StatResult:
    """Результат статистической обработки от Go-калькулятора."""

    sum: float
    mean: float
    min: float
    max: float
    stddev: float


class CalculatorClient:
    """Обёртка над Go-бинарём для статистических вычислений."""

    def __init__(self, binary_path: Path = BINARY_PATH) -> None:
        self._binary = binary_path

    def calculate(self, numbers: list[float]) -> StatResult:
        if not self._binary.exists():
            raise FileNotFoundError(
                f"Go binary not found: {self._binary}\n"
                "Run: cd go_app && go build -o calculator.exe ./cmd/calculator"
            )

        payload = json.dumps({"numbers": numbers}).encode()

        proc = subprocess.run(
            [str(self._binary)],
            input=payload,
            capture_output=True,
            timeout=10,
        )

        if proc.returncode != 0:
            raise RuntimeError(
                f"Go process failed (exit {proc.returncode}): "
                f"{proc.stderr.decode().strip()}"
            )

        data = json.loads(proc.stdout)
        return StatResult(**data)