from __future__ import annotations

import urllib.request
import json
from dataclasses import dataclass


SERVICE_URL = "http://localhost:8081"


@dataclass(frozen=True)
class StatsResult:

    count: int
    sum: float
    mean: float
    median: float
    min: float
    max: float
    stddev: float


class StatsServiceClient:

    def __init__(self, base_url: str = SERVICE_URL) -> None:
        self._base_url = base_url.rstrip("/")

    def calculate(self, numbers: list[float]) -> StatsResult:

        payload = json.dumps({"numbers": numbers}).encode()

        req = urllib.request.Request(
            f"{self._base_url}/stats",
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
                f"Cannot connect to stats service at {self._base_url}. "
                "Is it running? cd go_service && go run ./cmd/service"
            ) from e


if __name__ == "__main__":
    client = StatsServiceClient()
    result = client.calculate([10, 20, 30, 40, 50, 15, 25])
    print(f"Count:  {result.count}")
    print(f"Sum:    {result.sum}")
    print(f"Mean:   {result.mean}")
    print(f"Median: {result.median}")
    print(f"Min:    {result.min}")
    print(f"Max:    {result.max}")
    print(f"Stddev: {result.stddev}")