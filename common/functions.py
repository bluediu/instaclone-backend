# Core
import random
import string
from datetime import datetime, date

# Libs
import cloudinary.uploader


def upload_to_cloudinary(*, file, folder="avatars"):
    try:
        result = cloudinary.uploader.upload(file, folder=f"instaclone/{folder}")
        return result.get("secure_url"), None
    except Exception as e:
        return None, str(e)


def extract_public_id(image_url: str) -> str:
    """Extract public_id from a Cloudinary URL."""
    # Example URL: https://res.cloudinary.com/demo/image/instaclone/avatars/v12345678
    # /instaclone/avatars/v12345678
    return "/".join(image_url.split("/")[-3:]).split(".")[0]


def parse_date(date_str: str) -> date:
    """Parse a date string to date objects."""
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def clean_spaces(content: str) -> str:
    """Remove spaces from a string."""
    return " ".join(content.split())


def generate_random_code(length=6) -> str:
    """Return a random code."""
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))
