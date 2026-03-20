from __future__ import annotations

import json
import urllib.request
import urllib.error
from dataclasses import dataclass, asdict

import rustcrypto  # type: ignore[import]


SERVICE_URL = "http://localhost:8082"
CRYPTO_KEY = "lab9secret"


@dataclass(frozen=True)
class StatsResult:
    count: int
    sum: float
    mean: float
    median: float
    min: float
    max: float
    stddev: float


@dataclass(frozen=True)
class OrchestratedResult:
    stats: StatsResult
    encrypted: str
    decrypted: str


class Orchestrator:

    def __init__(self, service_url: str = SERVICE_URL, key: str = CRYPTO_KEY) -> None:
        self._service_url = service_url.rstrip("/")
        self._key = key

    def process(self, numbers: list[float]) -> OrchestratedResult:

        stats = self._fetch_stats(numbers)
        stats_json = json.dumps(asdict(stats))

        encrypted = rustcrypto.xor_encrypt(stats_json, self._key)
        decrypted = rustcrypto.xor_decrypt(encrypted, self._key)

        return OrchestratedResult(
            stats=stats,
            encrypted=encrypted,
            decrypted=decrypted,
        )

    def _fetch_stats(self, numbers: list[float]) -> StatsResult:
        payload = json.dumps({"numbers": numbers}).encode()
        req = urllib.request.Request(
            f"{self._service_url}/stats",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read())
                return StatsResult(**data)
        except urllib.error.HTTPError as e:
            body = json.loads(e.read())
            raise RuntimeError(f"Service error {e.code}: {body.get('error')}") from e
        except urllib.error.URLError as e:
            raise ConnectionError(
                f"Cannot connect to service at {self._service_url}. "
                "Run: cd go_service && go run ./cmd/service"
            ) from e


if __name__ == "__main__":
    orchestrator = Orchestrator()
    numbers = [10.0, 25.0, 30.0, 15.0, 50.0, 20.0, 40.0]

    print(f"Input: {numbers}\n")
    result = orchestrator.process(numbers)

    print("=== Statistics (from Go) ===")
    print(f"  Count:  {result.stats.count}")
    print(f"  Sum:    {result.stats.sum}")
    print(f"  Mean:   {result.stats.mean}")
    print(f"  Median: {result.stats.median}")
    print(f"  Min:    {result.stats.min}")
    print(f"  Max:    {result.stats.max}")
    print(f"  Stddev: {result.stats.stddev}")

    print("\n=== Crypto (from Rust) ===")
    print(f"  Encrypted (hex): {result.encrypted[:40]}...")
    print(f"  Decrypted:       {result.decrypted[:60]}...")
    print(f"  Roundtrip OK:    {result.decrypted == json.dumps(asdict(result.stats))}")