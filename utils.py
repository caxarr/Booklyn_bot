from datetime import datetime

TELEGRAM_MESSAGE_LIMIT = 4000


def chunk_text(text: str, limit: int = TELEGRAM_MESSAGE_LIMIT) -> list[str]:
    lines = text.split("\n")
    chunks: list[str] = []
    current = ""
    for line in lines:
        if len(current) + len(line) + 1 > limit:
            chunks.append(current)
            current = ""
        current += line + "\n"
    if current:
        chunks.append(current)
    return chunks


def is_valid_date(value: str) -> bool:
    try:
        datetime.strptime(value.strip(), "%d.%m")
        return True
    except ValueError:
        return False


def is_valid_time(value: str) -> bool:
    try:
        datetime.strptime(value.strip(), "%H:%M")
        return True
    except ValueError:
        return False
