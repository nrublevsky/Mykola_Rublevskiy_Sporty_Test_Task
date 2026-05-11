from datetime import date
from typing import Any, Callable

import pytest
import requests

from helpers.config import Config


@pytest.fixture
def build_headers() -> dict[str, str]:
    return {
        "x-user-id": Config.USER_ID,
        "Content-Type": "application/json",
    }


@pytest.fixture
def build_request_url() -> Callable[[str], str]:
    def _build(endpoint: str) -> str:
        return f"{Config.BASE_URL}{endpoint}"

    return _build


@pytest.fixture
def get_future_match(build_headers: dict[str, str], build_request_url: Callable[[str], str]) -> dict[str, Any]:
    response = requests.get(
        build_request_url(Config.MATCHES_ENDPOINT),
        headers=build_headers,
        timeout=10)

    matches: list[dict[str, Any]] = response.json()

    today = date.today()

    for match in matches:
        kickoff = date.fromisoformat(match["kickoffDate"])
        if kickoff >= today:
            return match

    pytest.fail("No future match found by GET /api/matches")


@pytest.fixture
def build_bet_payload(get_future_match: dict[str, Any]) -> Callable[..., dict[str, Any]]:
    def _build(
            stake: float,
            selection: str = Config.DEFAULT_SELECTION,
            match_id: str | None = None,
    ) -> dict[str, Any]:
        return {
            "matchId": match_id or get_future_match["id"],
            "selection": selection,
            "stake": stake,
        }

    return _build

@pytest.fixture
def reset_balance(build_headers: dict[str, str], build_request_url: Callable[[str], str]) -> None:
    response = requests.post(
        build_request_url(Config.RESET_BALANCE_ENDPOINT),
        headers=build_headers,
        timeout=10,
    )
    response.raise_for_status()