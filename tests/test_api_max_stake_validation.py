import pytest
import requests

from helpers.config import Config

@pytest.mark.api
@pytest.mark.parametrize("stake, expected_status, expected_message", [
    pytest.param(99, 200, "Bet placed successfully", id="stake_below_max"),
    pytest.param(99.99, 200, "Bet placed successfully", id="stake_decimal_below_max"),
    pytest.param(100, 200, "Bet placed successfully", id="stake_max"),
    pytest.param(100.01, 422, "Stake must be at most 100.00.", id="stake_decima_ove_max"),
    pytest.param(101, 422, "Stake must be at most 100.00.", id="stake_above_max")])
def test_api_max_stake_validation_bet_placement(
        build_headers,
        build_request_url,
        build_bet_payload,
        stake,
        expected_status,
        expected_message,
        reset_balance,
):
    """this tests a crucial validation for a central feature of tested app, Max stake"""
    # arrange - prepare data for test
    test_payload = build_bet_payload(stake=stake)

    # act - perform required action
    response = requests.post(build_request_url(Config.PLACE_BET_ENDPOINT), json=test_payload, headers=build_headers, timeout=10)

    #debug
    # print(response.text)

    # assert status and message
    assert response.status_code == expected_status, response.text

    response_json = response.json()
    assert response_json["message"] == expected_message

