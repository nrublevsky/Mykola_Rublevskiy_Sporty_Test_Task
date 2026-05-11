# Sporty Test Task

Pytest-based automation for the Sports Betting QA assignment.

The project currently contains:
- a parametrized API test for max stake validation
- a Selenium E2E UI test for the successful bet placement flow

## Prerequisites

- Python 3.13
- Google Chrome

## Setup

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run Tests

Run all tests:

```bash
python -m pytest -q
```

Run API tests only:

```bash
python -m pytest -m api -q
```

Run UI E2E tests only:

```bash
python -m pytest -m ui_e2e -q
```

Run UI tests in headless mode:

```bash
HEADLESS=1 python -m pytest -m ui_e2e -q
```

## Notes

- Tests target the hosted app: `https://qae-assignment-tau.vercel.app`
- Shared user context is configured in `helpers/config.py`
- UI automation uses Selenium with Chrome
