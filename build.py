import main
from languages import LANGS
import os

for language in LANGS:
    try:
        os.makedirs(os.path.dirname(f"{language}/"), exist_ok=True)
        main.build(lang=language)
    except Exception as e:
        print(f"Skipped {language} because Exception: {e}")
