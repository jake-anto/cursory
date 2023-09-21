import logging
import uuid
from datetime import datetime
from typing import Dict

import requests
from PIL import Image

from languages import LANGS

TODAY = datetime.utcnow().strftime("%Y/%m/%d")
API_URL = "https://api.wikimedia.org/"
HEADERS = {
    "User-Agent": f"CursoryBot/0.0.1 (https://github.com/jake-anto/cursory; cursory@itsjake.me) requests/{requests.__version__}"
}


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
    response = requests.get(
        API_URL + f"feed/v1/wikipedia/{lang}/featured/{TODAY}", headers=HEADERS
    )
    if response.status_code == 200:
        return response.json()


def optimize_image(link: str, lang: str) -> str:
    """Convert an image to WebP and save it to the site/lang/ directory.

    Parameters
    ----------
    link : str
        The link to the image to optimize.
    lang : str
        To determine the directory to save the image to.

    Returns
    -------
    str
        The link to the optimized image. If the image could not be optimized,
        the original link is returned.
    """
    try:
        file_id = uuid.uuid4().hex
        filename = f"site/{lang}/{file_id}.webp"

        image = Image.open(requests.get(link, stream=True, headers=HEADERS).raw)
        image.save(filename, format="webp")

        return f"/{lang}/{file_id}.webp"
    except Exception:
        logging.warning("Could not optimize image. Fallback to original link instead.")
        return link


def generate_sitemap(canonical_url: str) -> str:
    """Generate a sitemap for the given languages.

    Parameters
    ----------
    canonical_url : str
        The canonical URL of the site.

    Returns
    -------
    str
        The sitemap.
    """
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>{canonical_url}</loc>
        <lastmod>{datetime.utcnow()}</lastmod>
        <changefreq>daily</changefreq>
    </url>
    <url>
        <loc>{canonical_url}about</loc>
    </url>
    """

    for lang in LANGS:
        sitemap += f"""
        <url>
            <loc>{canonical_url}{lang}</loc>
            <lastmod>{datetime.utcnow()}</lastmod>
            <changefreq>daily</changefreq>
        </url>
        """

    sitemap += "</urlset>"

    return sitemap
