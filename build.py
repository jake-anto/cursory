import main
from languages import LANGS

for language in LANGS:
    try:
        main.build(lang=language)
    except Exception as e:
        print(f"Skipped {language} because Exception: {e}")
