from datetime import datetime
from typing import Dict

import requests

TODAY = datetime.utcnow().strftime("%Y/%m/%d")
API_URL = "https://api.wikimedia.org/"


def get_featured(lang="en") -> Dict:
    """Get the featured content for today from the Wikimedia API.

    Parameters
    ----------
    lang : str, optional
        The language to get the featured content for, by default 'en'

    Returns
    -------
    dict
        The featured content for today.
    """
    response = requests.get(API_URL + f"feed/v1/wikipedia/{lang}/featured/{TODAY}")
    if response.status_code == 200:
        return response.json()
