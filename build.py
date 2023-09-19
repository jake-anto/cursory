import main
from languages import LANGS
import os
import shutil

# Clear site directory
if os.path.isdir('site'):
    print("Clearing site directory")
    try:
        shutil.rmtree('site')
    except OSError as e:
        print(f"Error {e.filename} - {e.filename}.{e.strerror}")

for language in LANGS:
    try:
        # Create a directory for language
        os.makedirs(os.path.dirname(f"site/{language}/"), exist_ok=True)
        # Build HTML file
        main.build(lang=language)
    except Exception as e:
        print(f"Skipped {language} because Exception: {e}")
