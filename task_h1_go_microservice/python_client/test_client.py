from __future__ import annotations

import json
from io import BytesIO
from unittest.mock import MagicMock, patch
import urllib.error

import pytest

from client import StatsServiceClient, StatsResult


SAMPLE_RESPONSE = {
    "count": 5,
    "sum": 15.0,
    "mean": 3.0,
    "median": 3.0,
    "min": 1.0,
    "max": 5.0,
    "stddev": 1.414,
}


def _make_mock_response(data: dict, status: int = 200):
    mock = MagicMock()
    mock.read.return_value = json.dumps(data).encode()
    mock.status = status
    mock.__enter__ = lambda s: s
    mock.__exit__ = MagicMock(return_value=False)
    return mock


@pytest.fixture()
def client() -> StatsServiceClient:
    return StatsServiceClient(base_url="http://localhost:8081")


class TestStatsServiceClient:
    def test_returns_stats_result(self, client: StatsServiceClient) -> None:
        mock_resp = _make_mock_response(SAMPLE_RESPONSE)

        with patch("urllib.request.urlopen", return_value=mock_resp):
            result = client.calculate([1, 2, 3, 4, 5])

        assert isinstance(result, StatsResult)
        assert result.sum == 15.0
        assert result.mean == 3.0
        assert result.count == 5

    def test_raises_runtime_error_on_http_error(self, client: StatsServiceClient) -> None:
        error_body = json.dumps({"error": "input must contain at least one number"}).encode()
        http_error = urllib.error.HTTPError(
            url="http://localhost:8081/stats",
            code=400,
            msg="Bad Request",
            hdrs=None,
            fp=BytesIO(error_body),
        )

        with patch("urllib.request.urlopen", side_effect=http_error):
            with pytest.raises(RuntimeError, match="Service error 400"):
                client.calculate([])

    def test_raises_connection_error_when_service_down(self, client: StatsServiceClient) -> None:
        url_error = urllib.error.URLError(reason="Connection refused")

        with patch("urllib.request.urlopen", side_effect=url_error):
            with pytest.raises(ConnectionError, match="Cannot connect"):
                client.calculate([1, 2, 3])

    def test_sends_correct_payload(self, client: StatsServiceClient) -> None:
        mock_resp = _make_mock_response(SAMPLE_RESPONSE)

        with patch("urllib.request.urlopen", return_value=mock_resp):
            with patch("urllib.request.Request") as mock_req:
                mock_req.return_value = MagicMock()
                client.calculate([1.0, 2.0, 3.0])
                call_args = mock_req.call_args
                sent_data = json.loads(call_args.kwargs["data"])
                assert sent_data["numbers"] == [1.0, 2.0, 3.0]

    def test_result_fields_match_response(self, client: StatsServiceClient) -> None:
        mock_resp = _make_mock_response(SAMPLE_RESPONSE)

        with patch("urllib.request.urlopen", return_value=mock_resp):
            result = client.calculate([1, 2, 3, 4, 5])

        assert result.min == 1.0
        assert result.max == 5.0
        assert result.median == 3.0
        assert result.stddev == 1.414