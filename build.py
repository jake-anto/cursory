import logging
import os
import shutil
from time import time

import requests

import main
from languages import LANGS

# Begin timer
build_start = time()


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
