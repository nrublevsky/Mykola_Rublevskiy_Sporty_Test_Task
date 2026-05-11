from datetime import date, datetime
from typing import Callable

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BettingPage:
    DATE_FILTER_BUTTON = (By.CSS_SELECTOR, "button.dateFilterButton")
    CUSTOM_DATE_TAB = (By.XPATH, "//button[contains(@class,'dateFilterTab') and normalize-space()='Custom']")
    MONTH_LABEL = (By.ID, "month-label")
    PREV_MONTH_BUTTON = (By.ID, "prev-month")
    NEXT_MONTH_BUTTON = (By.ID, "next-month")
    APPLY_DATE_FILTER_BUTTON = (
        By.XPATH,
        "//div[@id='date-filter-popover']//button[contains(@class,'primaryBtn') and normalize-space()='Apply']",
    )

    STAKE_INPUT = (By.CSS_SELECTOR, "input.stakeInput")
    PLACE_BET_BUTTON = (By.CSS_SELECTOR, "button.placeBetButton")
    SUCCESS_RECEIPT_TITLE = (By.XPATH, "//*[normalize-space()='Bet Placed Successfully!']")
    RECEIPT_ROOT = (By.CSS_SELECTOR, "div.modalRoot")
    RECEIPT_CLOSE_BUTTON = (By.CSS_SELECTOR, "button.modalCloseButton")

    def __init__(
        self,
        driver: WebDriver,
        wait: WebDriverWait,
        build_app_url: Callable[[str], str],
    ) -> None:
        self.driver = driver
        self.wait = wait
        self.build_app_url = build_app_url

    def open(self) -> None:
        self.driver.get(self.build_app_url())

    def filter_by_single_date(self, target_date: date) -> None:
        self.wait.until(EC.element_to_be_clickable(self.DATE_FILTER_BUTTON)).click()
        self.wait.until(EC.element_to_be_clickable(self.CUSTOM_DATE_TAB)).click()
        self._navigate_calendar_to(target_date)
        self._click_day(target_date.day)
        self.wait.until(EC.element_to_be_clickable(self.APPLY_DATE_FILTER_BUTTON)).click()

    def select_home_outcome_for_match(self, home_team: str, away_team: str) -> None:
        card = self._match_card(home_team, away_team)
        home_odds_button = card.find_element(
            By.XPATH,
            ".//button[contains(@class,'oddsButton')][.//span[contains(@class,'oddsButtonLabel') and normalize-space()='1']]",
        )
        home_odds_button.click()

    def enter_stake(self, stake: str) -> None:
        stake_input = self.wait.until(EC.visibility_of_element_located(self.STAKE_INPUT))
        stake_input.clear()
        stake_input.send_keys(stake)

    def place_bet(self) -> None:
        self.wait.until(EC.element_to_be_clickable(self.PLACE_BET_BUTTON)).click()

    def wait_for_success_receipt(self) -> dict[str, str]:
        receipt_root = self.wait.until(EC.visibility_of_element_located(self.RECEIPT_ROOT))
        self.wait.until(EC.visibility_of_element_located(self.SUCCESS_RECEIPT_TITLE))

        return {
            "title": receipt_root.find_element(By.CSS_SELECTOR, "h2.modalTitle").text.strip(),
            "bet_id": receipt_root.find_element(By.CSS_SELECTOR, ".modalMono").text.strip(),
            "stake": receipt_root.find_element(
                By.XPATH,
                ".//div[contains(@class,'modalMicroLabel') and normalize-space()='Stake']/following-sibling::div[contains(@class,'modalValue')][1]",
            ).text.strip(),
        }

    def close_receipt(self) -> None:
        self.wait.until(EC.element_to_be_clickable(self.RECEIPT_CLOSE_BUTTON)).click()

    def _navigate_calendar_to(self, target_date: date) -> None:
        target_month = target_date.replace(day=1)

        while True:
            current_label = self.wait.until(EC.visibility_of_element_located(self.MONTH_LABEL)).text.strip()
            current_month = datetime.strptime(current_label, "%B %Y").date().replace(day=1)

            if current_month == target_month:
                return

            if current_month < target_month:
                self.wait.until(EC.element_to_be_clickable(self.NEXT_MONTH_BUTTON)).click()
            else:
                self.wait.until(EC.element_to_be_clickable(self.PREV_MONTH_BUTTON)).click()

    def _click_day(self, day_number: int) -> None:
        day_locator = (
            By.XPATH,
            f"//div[@id='date-filter-popover']//button[contains(@class,'dayCell') and normalize-space()='{day_number}']",
        )
        self.wait.until(EC.element_to_be_clickable(day_locator)).click()

    def _match_card(self, home_team: str, away_team: str):
        locator = (
            By.XPATH,
            "//div[contains(@class,'matchCard')]"
            f"[.//span[contains(@class,'teamName') and normalize-space()='{home_team}']]"
            f"[.//span[contains(@class,'teamName') and normalize-space()='{away_team}']]",
        )
        return self.wait.until(EC.visibility_of_element_located(locator))
