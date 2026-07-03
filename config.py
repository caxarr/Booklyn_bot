import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
DB_PATH = os.getenv("DB_PATH", "bookings.db")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set. Add it to your .env file.")
