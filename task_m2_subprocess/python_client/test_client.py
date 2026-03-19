"""Тесты для CalculatorClient (Go subprocess)."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from client import CalculatorClient, StatResult


@pytest.fixture()
def client(tmp_path: Path) -> CalculatorClient:
    fake_binary = tmp_path / "calculator.exe"
    fake_binary.touch()
    return CalculatorClient(binary_path=fake_binary)


def _make_stdout(data: dict) -> bytes:
    return json.dumps(data).encode()


class TestCalculatorClient:
    def test_returns_stat_result(self, client: CalculatorClient) -> None:
        response = {"sum": 15.0, "mean": 3.0, "min": 1.0, "max": 5.0, "stddev": 1.414}
        mock_result = MagicMock(returncode=0, stdout=_make_stdout(response), stderr=b"")

        with patch("subprocess.run", return_value=mock_result):
            result = client.calculate([1, 2, 3, 4, 5])

        assert isinstance(result, StatResult)
        assert result.sum == 15.0
        assert result.mean == 3.0
        assert result.min == 1.0
        assert result.max == 5.0

    def test_raises_on_nonzero_exit(self, client: CalculatorClient) -> None:
        mock_result = MagicMock(returncode=1, stdout=b"", stderr=b"some error")

        with patch("subprocess.run", return_value=mock_result):
            with pytest.raises(RuntimeError, match="Go process failed"):
                client.calculate([1, 2, 3])

    def test_raises_when_binary_missing(self, tmp_path: Path) -> None:
        client = CalculatorClient(binary_path=tmp_path / "nonexistent")
        with pytest.raises(FileNotFoundError):
            client.calculate([1, 2, 3])

    def test_passes_numbers_as_json(self, client: CalculatorClient) -> None:
        response = {"sum": 3.0, "mean": 1.5, "min": 1.0, "max": 2.0, "stddev": 0.5}
        mock_result = MagicMock(returncode=0, stdout=_make_stdout(response), stderr=b"")

        with patch("subprocess.run", return_value=mock_result) as mock_run:
            client.calculate([1.0, 2.0])
            sent_input = mock_run.call_args.kwargs["input"]
            data = json.loads(sent_input)
            assert data["numbers"] == [1.0, 2.0]

    def test_empty_list_returns_zeros(self, client: CalculatorClient) -> None:
        response = {"sum": 0.0, "mean": 0.0, "min": 0.0, "max": 0.0, "stddev": 0.0}
        mock_result = MagicMock(returncode=0, stdout=_make_stdout(response), stderr=b"")

        with patch("subprocess.run", return_value=mock_result):
            result = client.calculate([])

        assert result.sum == 0.0