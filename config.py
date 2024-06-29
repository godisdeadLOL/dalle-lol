import os

API_KEYS = os.environ["API_KEYS"].split(",")
TOKEN = os.environ["TOKEN"]

BASE_URL = "https://api.openai.com/v1"
TIMEOUT = 60

PLAIN_ERROR = "Generation error"
