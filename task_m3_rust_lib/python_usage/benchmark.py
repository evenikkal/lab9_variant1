from __future__ import annotations

import time

import fastmath  # type: ignore[import]


def sum_squares_python(numbers: list[int]) -> int:
    return sum(x * x for x in numbers)


def benchmark(label: str, fn, numbers: list[int], iterations: int = 1000) -> float:
    start = time.perf_counter()
    for _ in range(iterations):
        fn(numbers)
    elapsed = time.perf_counter() - start
    avg_ms = (elapsed / iterations) * 1000
    print(f"{label:20s}: {avg_ms:.4f} ms (avg over {iterations} runs)")
    return avg_ms


def main() -> None:
    numbers = list(range(1, 10_001))  

    print(f"Input: list of {len(numbers)} integers\n")

    rust_time = benchmark("Rust (fastmath)", fastmath.sum_squares, numbers)
    python_time = benchmark("Python (pure)", sum_squares_python, numbers)

    speedup = python_time / rust_time
    print(f"\nRust is {speedup:.1f}x faster than Python")

    assert fastmath.sum_squares([1, 2, 3, 4, 5]) == 55
    assert sum_squares_python([1, 2, 3, 4, 5]) == 55
    print("\nCorrectness check passed ✓")


if __name__ == "__main__":
    main()