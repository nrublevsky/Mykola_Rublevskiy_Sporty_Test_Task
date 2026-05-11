from datetime import date
from typing import Any, Callable, Generator

import pytest
import requests
from selenium.webdriver.chrome.webdriver import WebDriver

from helpers.config import Config

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from pom.betting_page import BettingPage

# __________________API_____________________
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

@pytest.fixture(scope="function")
def reset_balance(build_headers: dict[str, str], build_request_url: Callable[[str], str]) -> None:
    response = requests.post(
        build_request_url(Config.RESET_BALANCE_ENDPOINT),
        headers=build_headers,
        timeout=10,
    )
    response.raise_for_status()



# __________________UI_____________________



@pytest.fixture(scope="session")
def build_app_url() -> Callable[[str], str]:
    def _build(user_id: str = Config.USER_ID) -> str:
        return f"{Config.BASE_URL}{Config.HOME_PATH}?user-id={user_id}"

    return _build

@pytest.fixture(scope="function")
def driver(reset_balance) -> Generator[WebDriver, Any, None]:
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    if Config.HEADLESS:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    chrome_driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options,
    )

    yield chrome_driver
    chrome_driver.quit()

@pytest.fixture(scope="function")
def ui_wait(driver: webdriver.Chrome) -> WebDriverWait:
    return WebDriverWait(driver, Config.EXPLICIT_WAIT_SECONDS)

@pytest.fixture(scope="function")
def betting_page(
        driver: webdriver.Chrome,
        ui_wait: WebDriverWait,
        build_app_url: Callable[[str], str],
) -> BettingPage:
    return BettingPage(driver=driver, wait=ui_wait, build_app_url=build_app_url)
