# Bug Reports

### Note: There are quite a lot of bugs and mismatches with requirements in almost every aspect of test-app. I've listed those related to betting flow and balance.

#### SBQA-BR1 - FE: User is able to place a bet for a match in the past
#### SBQA-BR2 - FE: Balance is not updated after successful bet placement
#### SBQA-BR3 - FE: User is able to place several consecutive bets in a single session, causing negative balance
#### SBQA-BR4 - API: Reset balance API returns 120 instead of expected initial value 125.5
#### SBQA-BR5 - UI: Potential payout differs between Bet Slip and bet success receipt

_________
## SBQA-BR1 - FE: User is able to place a bet for a match in the past
### Related Test: _**SBQA-TC2**_
### Severity: **Critical**
#### Reproduction steps:

- Preconditions: User logged in and in "betting screen".
- Open Date filter
- Select a past single date or date range that returns already finished matches
- Verify the match list shows returned past matches
- Click any available Odd button for one returned match
- Enter valid Stake amount in Bet Slip view (e.g. 10.00)
- Click Place Bet

#### Expected Result: Bet placement is rejected for the selected past match, an error state is shown, and Available Balance remains unchanged.
#### Actual Result: Bet Receipt for successful bet is displayed. Bet is deducted from balance.

#### Business Impact: Users can spend real balance on invalid historical events, which breaks a core betting rule, creates direct financial risk, and undermines trust in settlement integrity.
#### Environment:
URL: https://qae-assignment-tau.vercel.app/?user-id=candidate-g7Td4Yn2MJ
Platform: Web
Browser: Chrome Version 148.0.7778.97 (Official Build) (64-bit)
#### Evidence:

_________
## SBQA-BR2 - FE: Balance is not updated after successful bet placement
### Related Test: _**SBQA-TC3**_
### Severity: **High**
#### Reproduction steps:

- Preconditions: User logged in and in "betting screen". User has sufficient funds for a bet.
- Note currently displayed Available Balance
- Find any upcoming match in the match list
- Click any Odd button for the selected match
- Enter valid Stake amount in Bet Slip view (e.g. 10.00)
- Calculate expected updated balance as: initial balance - entered stake
- Click Place Bet
- Wait for successful Bet Receipt modal to appear
- Close Bet Receipt modal
- Observe Available Balance in main betting flow

#### Expected Result: Bet is placed successfully and Available Balance is reduced exactly once by the entered stake amount. Updated balance matches the expected calculated value and remains visible after closing the receipt.
#### Actual Result: Bet is placed successfully and Bet Receipt modal is displayed, but Available Balance in the main betting flow is not updated to the expected deducted value after the successful placement.

#### Business Impact: Users see misleading available funds after a successful transaction, which can cause incorrect betting decisions, failed follow-up bets, and reduced trust in account balance accuracy.
#### Environment:
URL: https://qae-assignment-tau.vercel.app/?user-id=candidate-g7Td4Yn2MJ
Platform: Web
Browser: Chrome Version 148.0.7778.97 (Official Build) (64-bit)
#### Evidence:

_________
## SBQA-BR3 - FE: User is able to place several consecutive bets in a single session, causing negative balance
### Related Test: _**SBQA-TC3**_
### Severity: **Medium**
#### Reproduction steps:

- Preconditions: User logged in and in "betting screen". User has limited available balance that can be exceeded by placing several valid bets in sequence.
- Note currently displayed Available Balance
- Find any upcoming match in the match list
- Click any Odd button for the selected match
- Enter valid Stake amount in Bet Slip view that is lower than current balance
- Click Place Bet
- Wait for successful Bet Receipt modal to appear
- Close Bet Receipt modal
- Repeat the same flow with additional valid bets during the same session until the total deducted stake exceeds the starting balance
- Observe Available Balance after the final successful placement

#### Expected Result: Once the remaining balance is insufficient, further bet placement should be rejected and Available Balance must never drop below zero.
#### Actual Result: The application continues accepting consecutive successful bets during the same session even after available funds should be exhausted, resulting in a negative balance.

#### Business Impact: Users can overspend beyond their available funds, creating direct financial exposure, invalid account state, and high-risk reconciliation issues for the platform.
#### Environment:
URL: https://qae-assignment-tau.vercel.app/?user-id=candidate-g7Td4Yn2MJ
Platform: Web
Browser: Chrome Version 148.0.7778.97 (Official Build) (64-bit)
#### Evidence:

_________
## SBQA-BR4 - API: Reset balance API returns 120 instead of expected initial value 125.5
### Related Test: _**Exploratory API validation**_
### Severity: **Low**
#### Reproduction steps:

- Preconditions: API client is authorized with a valid `x-user-id` header.
- Send `POST /api/reset-balance` with a valid `x-user-id`
- Inspect the response body `balance` value
- Optionally send `GET /api/balance` with the same `x-user-id`
- Compare the returned balance value with the expected initial configured value `125.5`

#### Expected Result: `POST /api/reset-balance` resets the user balance to the configured initial value `125.5`, and the persisted balance returned by `GET /api/balance` matches that same value.
#### Actual Result: `POST /api/reset-balance` resets the balance to `120` instead of `125.5`.

#### Business Impact: Resetting users to the wrong baseline balance produces incorrect financial state, affects repeatability of tests and sessions, and can mask or create downstream balance-related defects.
#### Environment:
URL: https://qae-assignment-tau.vercel.app/?user-id=candidate-g7Td4Yn2MJ
Platform: Web / API
Browser: Chrome Version 148.0.7778.97 (Official Build) (64-bit)
#### Evidence:

_________
## SBQA-BR5 - UI: Potential payout differs between Bet Slip and bet success receipt
### Related Test: _**SBQA-TC4**_
### Severity: **Low**
#### Reproduction steps:

- Preconditions: User logged in and in "betting screen". User has sufficient funds for a bet.
- Find any upcoming match in the match list
- Note the selected Odd value for one outcome
- Click that Odd button
- Enter valid Stake amount in Bet Slip view (e.g. 10.00)
- Note the Potential Payout value shown in Bet Slip before placement
- Click Place Bet
- Wait for successful Bet Receipt modal to appear
- Compare the Potential Payout value shown in the receipt with the value previously displayed in Bet Slip

#### Expected Result: Potential Payout in Bet Slip matches the Potential Payout shown in the success receipt for the same placed bet.
#### Actual Result: Potential Payout value shown in the success receipt differs from the value previously displayed in Bet Slip for the same stake and selected odds.

#### Business Impact: Users receive inconsistent win estimates across the same betting flow, which damages trust in payout accuracy and can lead to disputes around expected returns.
#### Environment:
URL: https://qae-assignment-tau.vercel.app/?user-id=candidate-g7Td4Yn2MJ
Platform: Web
Browser: Chrome Version 148.0.7778.97 (Official Build) (64-bit)
#### Evidence:

_________
## SBQA-BR6 - API: /api/place-bet returns currency as "USD"
### Related Test: _**test_api_max_stake_validation.py**_
### Severity: **High**
#### Reproduction steps:

- Preconditions: API client is authorized with a valid `x-user-id` header.
- Send `POST /api/place-bet` with a valid payload
- Inspect the response body `currency` value
- Compare the returned balance value with the expected initial configured value `EUR`

#### Expected Result: `POST /api/place_bet` returns response with "currency":"EUR".
#### Actual Result: `POST /api/place_bet` returns response with "currency":"USD".

#### Business Impact: Returning the wrong currency in bet placement responses creates financial inconsistency between API and UI, can mislead users about the value of their funds and payouts, and increases the risk of settlement, reporting, and integration errors.
#### Environment:
URL: https://qae-assignment-tau.vercel.app/?user-id=candidate-g7Td4Yn2MJ
Platform: Web / API
Browser: Chrome Version 148.0.7778.97 (Official Build) (64-bit)
#### Evidence:
