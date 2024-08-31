from datetime import datetime, date


def parse_date(date_str: str) -> date:
    """Parse a date string to date objects."""
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def clean_spaces(content: str) -> str:
    """Remove spaces from a string."""
    return " ".join(content.split())
