# Booklyn Bot

A Telegram bot for booking consultations / services, built with [aiogram](https://docs.aiogram.dev/) 3 and SQLite.

## Features

- `/start` — greeting and short explanation of what the bot does
- `/book` (or the "Записатись" button) — step-by-step booking flow (FSM):
  1. Asks for the user's name
  2. Asks for the desired date (`DD.MM`, e.g. `10.07`)
  3. Asks for the desired time (`HH:MM`, e.g. `14:30`)
  4. Asks for a short description of the request/service
  5. Shows a summary and asks for confirmation before saving
- `/my_bookings` — shows the user's own active bookings
- `/cancel` — cancels a booking currently being filled in (resets the FSM state)
- `/all_bookings` — admin-only command that lists every booking in the system

Invalid date/time input is rejected with a friendly message asking the user to try again — the bot never crashes on bad input.

## Project structure

```
Booklyn_bot/
├── main.py            # entry point: bot/dispatcher setup, polling
├── config.py           # loads settings from .env
├── database.py         # SQLite (aiosqlite) access layer
├── keyboards.py         # reply/inline keyboards
├── states.py            # FSM states for the booking flow
├── utils.py             # date/time validation, message chunking
├── handlers/
│   ├── __init__.py      # aggregates all routers
│   ├── start.py          # /start, /help
│   ├── booking.py         # booking FSM, /cancel, /my_bookings
│   └── admin.py            # /all_bookings (admin only)
├── requirements.txt
├── .env.example
└── .gitignore
```

## Database

SQLite table `bookings`:

| Column       | Type    | Notes                                      |
|--------------|---------|---------------------------------------------|
| id           | INTEGER | primary key, autoincrement                  |
| user_id      | INTEGER | Telegram user id                             |
| username     | TEXT    | Telegram @username (nullable)                |
| name         | TEXT    | name provided during booking                 |
| date         | TEXT    | requested date, `DD.MM`                      |
| time         | TEXT    | requested time, `HH:MM`                      |
| description  | TEXT    | short description of the request             |
| status       | TEXT    | `pending` / `confirmed` / `cancelled`         |
| created_at   | TEXT    | ISO 8601 UTC timestamp                        |

The database file is created automatically on first run.

## Setup

### 1. Clone and enter the project

```bash
git clone <your-repo-url>
cd Booklyn_bot
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example file and fill in your values:

```bash
cp .env.example .env
```

Edit `.env`:

```
BOT_TOKEN=123456789:AAExampleTokenReplaceWithYourOwn
ADMIN_ID=123456789
DB_PATH=bookings.db
```

- `BOT_TOKEN` — get it from [@BotFather](https://t.me/BotFather) on Telegram.
- `ADMIN_ID` — your numeric Telegram user id (you can get it from [@userinfobot](https://t.me/userinfobot)). Only this id can use `/all_bookings`.
- `DB_PATH` — optional, path to the SQLite file (defaults to `bookings.db` in the project root).

### 5. Run the bot

```bash
python main.py
```

The bot uses long polling, so no public URL or webhook setup is required.

## Notes

- FSM state is kept in memory (`MemoryStorage`); it resets if the bot restarts. For production use with multiple workers, consider `RedisStorage`.
- All user-facing text is in Ukrainian; adjust the strings in `handlers/` and `keyboards.py` if you need another language.
