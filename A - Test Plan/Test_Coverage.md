# Test Plan
## Details

- Document Analyzed: _**Feature_Specification.pdf**_
- Version: v1

### Short summary and scope

Users can place a single bet on a sports event outcome. This is the core betting functionality
that allows customers to wager money on match results with odds.

Scope:
- Platform: Desktop web application 
- Sport: Soccer/Football only 
- Event Type: Upcoming/Pre-match events only (no live betting)
- Bet Type: Single bet only (no accumulator/multi-bets)

Out of scope:
- Live betting 
- Multi-bets/accumulators 
- Other sports 
- Mobile-specific UX requirements


### Test Focus Areas

- Business Rules

  - match related (sport type, event type)
  - bet related (amount of bets, stake min\max)
  - odds related (odds min\max, behavior)

- FE

  - match list view and interaction
  - bet slip view and interaction
  - bet and balance calculations
  - bet receipt view and interaction
  - BE \ API integration
  - validations

- BE \ API

  - contract
  - request\response
  - schemas
  - validations


### High Risk Areas

- match list display and interaction
- bet \ payout calculations
- valid \ invalid match bet placement
- balance interaction after success, failure or reset

### Assumptions and considerations (should be clarified)

- Balance represents amount of money player has in his account within the system
- Payment system integration is out of scope
- Odds filtering returns all matches where any odd satisfies filter query
- Balance resetting is part of 

# Tests

### [SBQA-TC1] - Verify user can place a bet with sufficient amount for an upcoming match
### [SBQA-TC2] - Verify user can't bet on a match that already happened
### [SBQA-TC3] - Verify Balance is updated after every successful bet placement
### [SBQA-TC4] - Verify Potential Payout value is calculated consistently across Bet Placing Flow
### [SBQA-TC5] - Verify Odds filter max value can't be lower than min value
### [SBQA-TC6] - Verify "Showing N matches" displays correct amount of matches after applying filters
###
_______________
### [SBQA-TC1] - Verify user can place a bet with sufficient amount for an upcoming match
#### Priority: **Critical**
#### Risk Rationale: _Crucial happy-path E2E flow_ 
#### Steps:

Preconditions: User logged in and in "betting screen". User has sufficient funds for a bet.

- Open Date filter
- Select a future single date or date range that contains upcoming matches
- Verify the match list returns available upcoming football matches
- Click any Odd button for one returned match
- Enter valid Stake amount in Bet Slip view (e.g. 10.00)
- Verify Potential Payout is displayed
- Click Place Bet
- Wait for successful Bet Receipt modal to appear
#### Expected Result: Bet is placed successfully for the selected upcoming match and Bet Receipt modal is displayed with the placed bet details.

_______________
### [SBQA-TC2] - Verify user can't bet on a match that already happened
#### Priority: **Critical**
#### Risk Rationale: _Error-proofing user's behavior is important, especially if it may lead to user loosing real money_ 
#### Steps:

Preconditions: User logged in and in "betting screen".

- Note currently displayed Available Balance
- Open Date filter
- Select a past single date or date range that returns already finished matches
- Verify the match list shows returned past matches
- Click any available Odd button for one returned match
- Enter valid Stake amount in Bet Slip view (e.g. 10.00)
- Click Place Bet
#### Expected Result: Bet placement is rejected for the selected past match, an error state is shown, and Available Balance remains unchanged.

_______________
### [SBQA-TC3] - Verify Balance is updated after every successful bet placement
#### Priority: **Critical**
#### Risk Rationale: _Actual and accurate balance display is crucial_ 
#### Steps:

Preconditions: User logged in and in "betting screen". User has sufficient funds for a bet.

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

_______________
### [SBQA-TC4] - Verify Potential Payout value is calculated consistently across Bet Placing Flow
#### Priority: High
#### Risk Rationale: _Discrepancies in displaying possible win amount may look untrustworthy_ 
#### Steps:

Preconditions: User logged in and in "betting screen". User has sufficient funds for a bet.

- Find any upcoming match in the match list
- Note the selected Odd value for one outcome
- Click that Odd button
- Enter valid Stake amount in Bet Slip view (e.g. 10.00)
- Calculate expected Potential Payout as: stake x odd
- Verify Potential Payout value shown in Bet Slip matches the expected calculation
- Click Place Bet
- Wait for successful Bet Receipt modal to appear
- Verify Odds at placement and Potential Payout values shown in the receipt
#### Expected Result: Potential Payout in Bet Slip is calculated correctly from Stake and selected Odds. The same payout value is preserved in the success receipt and matches the final placed bet details.

_______________
### [SBQA-TC5] - Verify Odds filter max value can't be lower than min value
#### Priority: Medium
#### Risk Rationale: _Common sense_ 
#### Steps:

Preconditions: User logged in and in "betting screen".

- Open Odds filter
- Enter valid Min Odds value (e.g. 2.50)
- Enter lower Max Odds value than Min Odds (e.g. 1.50)
- Click outside the input or otherwise trigger field validation
- Attempt to apply the filter
#### Expected Result: Invalid odds range is rejected with clear user feedback. Filter is not applied while Max Odds is lower than Min Odds, and Apply action remains blocked.

_______________
### [SBQA-TC6] - Verify "Showing N matches" displays correct amount of matches after applying filters
#### Priority: Low
#### Risk Rationale: _Common sense and responsive UI practices_ 
#### Steps:

Preconditions: User logged in and in "betting screen".

- Note the current value displayed in the `Showing N matches` label
- Open Date filter
- Apply a filter that narrows the visible match list to a smaller subset
- If needed, additionally apply valid Odds filter values to further reduce the result set
- Count the number of visible match rows returned in the match list after filters are applied
- Compare the counted rows with the value shown in the `Showing N matches` label
#### Expected Result: `Showing N matches` displays the exact number of visible matches returned after the selected filters are applied.
