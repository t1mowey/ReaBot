import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
font = os.getenv('FONT')
MY_ID = int(os.getenv("MY_ID"))
MODE = os.getenv("MODE", "dev")

CALENDAR_LINK = os.getenv("CALENDAR_LINK")
BASE_URL = os.getenv("BASE_URL")
