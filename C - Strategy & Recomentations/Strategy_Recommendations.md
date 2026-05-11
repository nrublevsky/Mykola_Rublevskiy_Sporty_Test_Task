#### Why you selected these 2 tests for automation over other candidates

- For E2E I've selected basic happy path case, considering it is critical and crucial for it to work.
- For API I've selected Max stack validation, as it is a good example of "automate to saves time" test, and also demonstrate useful Parametrisation feature of Pytest. 

#### What you intentionally left as manual only and why

UI tests that verify element layout and visual behavior, like odds sliders and calendar date selection. 

#### Your top 2–3 recommendations if this project were to scale (CI/CD, additional test layers, data strategy, spec clarifications, etc)

Based on the spec and quick exploratory testing results I'd suggest:

- Spec clarification - there are conflicting requirements 
- Unit tests for calculations and validations
- Run critical tests on every commit (basic API\BE validations and small e2e suit for main user journeys)