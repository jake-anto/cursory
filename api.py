from datetime import datetime
from typing import Dict

import requests

LANG = "en"
TODAY = datetime.utcnow().strftime("%Y/%m/%d")
API_URL = f"https://api.wikimedia.org/feed/v1/wikipedia/{LANG}/featured/{TODAY}"


def get_featured() -> Dict:
    """Get the featured content for today from the Wikimedia API.

    Returns
    -------
    dict
        The featured content for today.
    """
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
