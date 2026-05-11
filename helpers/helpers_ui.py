from typing import Callable

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from helpers.config import Config
from pom.betting_page import BettingPage


@pytest.fixture(scope="session")
def build_app_url() -> Callable[[str], str]:
    def _build(user_id: str = Config.USER_ID) -> str:
        return f"{Config.BASE_URL}{Config.HOME_PATH}?user-id={user_id}"

    return _build


@pytest.fixture(scope="function")
def driver(reset_balance) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

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