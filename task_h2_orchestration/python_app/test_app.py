from __future__ import annotations

import json
from dataclasses import asdict
from io import BytesIO
from unittest.mock import MagicMock, patch
import urllib.error

import pytest

from app import Orchestrator, OrchestratedResult, StatsResult


SAMPLE_STATS = {
    "count": 3,
    "sum": 6.0,
    "mean": 2.0,
    "median": 2.0,
    "min": 1.0,
    "max": 3.0,
    "stddev": 0.816,
}


def _make_mock_response(data: dict):
    mock = MagicMock()
    mock.read.return_value = json.dumps(data).encode()
    mock.__enter__ = lambda s: s
    mock.__exit__ = MagicMock(return_value=False)
    return mock


@pytest.fixture()
def orchestrator() -> Orchestrator:
    return Orchestrator(service_url="http://localhost:8082", key="testkey")


class TestOrchestrator:
    def test_returns_orchestrated_result(self, orchestrator: Orchestrator) -> None:
        mock_resp = _make_mock_response(SAMPLE_STATS)

        with patch("urllib.request.urlopen", return_value=mock_resp):
            result = orchestrator.process([1.0, 2.0, 3.0])

        assert isinstance(result, OrchestratedResult)
        assert isinstance(result.stats, StatsResult)
        assert result.stats.sum == 6.0

    def test_encrypted_differs_from_plaintext(self, orchestrator: Orchestrator) -> None:
        mock_resp = _make_mock_response(SAMPLE_STATS)

        with patch("urllib.request.urlopen", return_value=mock_resp):
            result = orchestrator.process([1.0, 2.0, 3.0])

        stats_json = json.dumps(asdict(result.stats))
        assert result.encrypted != stats_json

    def test_decrypt_roundtrip(self, orchestrator: Orchestrator) -> None:
        mock_resp = _make_mock_response(SAMPLE_STATS)

        with patch("urllib.request.urlopen", return_value=mock_resp):
            result = orchestrator.process([1.0, 2.0, 3.0])

        assert result.decrypted == json.dumps(asdict(result.stats))

    def test_raises_on_service_error(self, orchestrator: Orchestrator) -> None:
        error_body = json.dumps({"error": "input must contain at least one number"}).encode()
        http_error = urllib.error.HTTPError(
            url="http://localhost:8082/stats",
            code=400,
            msg="Bad Request",
            hdrs=None,
            fp=BytesIO(error_body),
        )

        with patch("urllib.request.urlopen", side_effect=http_error):
            with pytest.raises(RuntimeError, match="Service error 400"):
                orchestrator.process([])

    def test_raises_on_connection_error(self, orchestrator: Orchestrator) -> None:
        with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("refused")):
            with pytest.raises(ConnectionError, match="Cannot connect"):
                orchestrator.process([1.0, 2.0])