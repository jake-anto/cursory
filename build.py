import logging
import os
import shutil
from time import time

import requests
import toml

import api
import main
from languages import LANGS

# Begin timer
build_start = time()

# Load config
config = toml.load("config.toml")

# Generate sitemap.xml if enabled
if config["site"]["generate_sitemap"]:
    start = time()

    with open("assets/sitemap.xml", "w", encoding="utf-8") as file:
        file.write(api.generate_sitemap(config["site"]["url"]))
    # Add sitemap to robots.txt
    with open("assets/robots.txt", "a") as file:
        file.write(f"\nSitemap: {config['site']['url']}sitemap.xml")

    print(f"Generated sitemap.xml in {round(time() - start, 3)}s")

# Self-host simple.css
start = time()

response = requests.get("https://cdn.simplecss.org/simple.min.css/")
with open("assets/simple.css", "w", encoding="utf-8") as file:
    file.write(response.text)

print(f"Downloaded simple.css in {round(time() - start, 3)}s")


# Clear site/ directory
start = time()

if os.path.isdir("site"):
    try:
        shutil.rmtree("site")
    except OSError as e:
        print(f"Error {e.filename} - {e.filename}.{e.strerror}")

print(f"Cleared site/ directory in {round(time() - start, 3)}s")

# Copy static assets
start = time()

shutil.copytree("assets/", "site/")

print(f"Copied static files in {round(time() - start, 3)}s")

for language in LANGS:
    try:
        start = time()

        # Create a directory for language
        os.makedirs(os.path.dirname(f"site/{language}/"), exist_ok=True)

        # Build HTML file
        main.build(lang=language)

        print(f"Built {language}.html in {round(time() - start, 3)}s")
    except Exception as e:
        logging.warning("Skipped %s.html because Exception: %s", language, e)

print(f"Build completed in {round(time() - build_start, 3)}")
