import main
from languages import LANGS
import os

for language in LANGS:
    try:
        # Create a directory for language
        os.makedirs(os.path.dirname(f"site/{language}/"), exist_ok=True)
        # Build HTML file
        main.build(lang=language)
    except Exception as e:
        print(f"Skipped {language} because Exception: {e}")
