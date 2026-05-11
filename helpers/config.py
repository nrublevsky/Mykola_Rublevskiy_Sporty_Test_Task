import os


class Config:
    USER_ID = "candidate-g7Td4Yn2MJ"

    BASE_URL = "https://qae-assignment-tau.vercel.app"
    HOME_PATH = "/"

    MATCHES_ENDPOINT = "/api/matches"
    PLACE_BET_ENDPOINT = "/api/place-bet"
    RESET_BALANCE_ENDPOINT = "/api/reset-balance"

    DEFAULT_SELECTION = "HOME"
    DEFAULT_UI_STAKE = "10.00"
    EXPLICIT_WAIT_SECONDS = 10
    HEADLESS = os.getenv("HEADLESS", "0") == "1"
