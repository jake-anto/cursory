import os
import shutil

import requests

import main
from languages import LANGS

# Self-host simple.css
print("Downloading simple.css")
response = requests.get("https://cdn.simplecss.org/simple.min.css/")
with open('assets/simple.css', "w", encoding="utf-8") as file:
    file.write(response.text)

# Clear site directory
if os.path.isdir('site'):
    print("Clearing site directory")
    try:
        shutil.rmtree('site')
    except OSError as e:
        print(f"Error {e.filename} - {e.filename}.{e.strerror}")

# Copy assets
shutil.copytree('assets/', 'site/')
print("Copied static files")

for language in LANGS:
    try:
        # Create a directory for language
        os.makedirs(os.path.dirname(f"site/{language}/"), exist_ok=True)
        # Build HTML file
        main.build(lang=language)
    except Exception as e:
        print(f"Skipped {language} because Exception: {e}")

print("Build complete")
