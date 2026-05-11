from datetime import date

import pytest

from helpers.config import Config


@pytest.mark.ui_e2e
def test_ui_e2e_place_bet_successful_flow(betting_page, get_future_match):
    target_date = date.fromisoformat(get_future_match["kickoffDate"])
    home_team = get_future_match["homeTeam"]
    away_team = get_future_match["awayTeam"]

    betting_page.open()
    betting_page.filter_by_single_date(target_date)
    betting_page.select_home_outcome_for_match(home_team, away_team)
    betting_page.enter_stake(Config.DEFAULT_UI_STAKE)
    betting_page.place_bet()

    receipt = betting_page.wait_for_success_receipt()

    assert receipt["title"] == "Bet Placed Successfully!"
    assert receipt["bet_id"].startswith("#B-")
    assert receipt["stake"] == f"€{Config.DEFAULT_UI_STAKE}"
